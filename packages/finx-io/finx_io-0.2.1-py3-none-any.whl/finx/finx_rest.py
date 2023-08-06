import asyncio
import dateutil.parser as dateparser
import functools
import json
import os
import numpy as np
import pandas as pd
import requests
import time
import websockets
from typing import Callable, Coroutine, List, Optional, Union
from enum import Enum


class FunctionEndpoints(Enum):
    prod = 'wss://prod.finx.io/streamer/{}'
    dev = 'wss://beta.finx.io/streamer/{}'
    prod_rest = 'https://prod.finx.io/backend/'
    dev_rest = 'https://beta.finx.io/backend/'

    @staticmethod
    def get_url(environment: str = 'dev', api_key: str = 'public'):
        try:
            return FunctionEndpoints[environment].value.format(api_key)
        except KeyError:
            return ''


def task_runner(task: Coroutine):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    run_loop = (loop.is_running() and loop.create_task) or loop.run_until_complete
    try:
        return run_loop(task)
    except TypeError:
        raise Exception('BAD LOOP PARAMS')


class Hybrid:

    def __init__(self, func: Callable):
        self._func = func
        self._func_name = func.__name__
        self._func_path = func.__name__
        self._func_class = None
        functools.update_wrapper(self, func)

    def __get__(self, obj, objtype):
        """Support instance methods."""
        self._func_class = obj
        return self

    def __call__(self, *args, **kwargs):
        return task_runner(self.run_func(*args, **kwargs))

    async def run_func(self, *args, **kwargs):
        if self._func_class is not None:
            args = (self._func_class,) + args
        return await self._func(*args, **kwargs)

    async def run_async(self, *args, **kwargs):
        return await self.run_func(*args, **kwargs)


class FinXRest:

    def __init__(self, finx_api_key: str = 'public', environment: str = "dev"):
        self.api_key = finx_api_key or os.getenv('FINX_API_KEY')
        self.endpoint = FunctionEndpoints.get_url(environment, self.api_key)
        self.rest_endpoint = FunctionEndpoints.get_url(f'{environment}_rest')
        print('-----> FinXRest Client Initialized -----> ')
        print('-----> user: ' + finx_api_key + ' -----> ')

    async def __aenter__(self):
        print('-----> Python SDK Connecting ----->')
        print('-----> endpoint: ' + self.endpoint + ' ----->')
        self._conn = websockets.connect(self.endpoint)
        self.websocket = await self._conn.__aenter__()
        is_auth = await self._authenticate()
        print('-----> FinX API Key authenticated -----> ', is_auth)
        #TODO: update the connection checker to a check_connection function
        result = await self._dispatch(
            dict(
                APIKey=self.api_key,
                pair='BTC:USDC',
                functionName='tickSnap'
            )
        )
        print('TickPlant connection test:', result)
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def __send(self, message: dict):
        message.update(APIKey=self.api_key)
        await self.websocket.send(json.dumps(message))

    async def __receive(self):
        return await self.websocket.recv()

    async def _dispatch(self, message: dict):
        await self.__send(message)
        print(self.websocket)
        return await self.__receive()

    @Hybrid
    async def _authenticate(self) -> dict:
        is_auth = await self._dispatch(
            dict(
                APIKey=self.api_key,
                functionName='authenticate'
            )
        )
        return is_auth

    def get_reference_data(self, security_id: str, unix_time: str = None) -> dict:
        response = requests.get(
            f'{self.rest_endpoint}reference/secdb/?APIKey={self.api_key}&securityId={security_id}'
        ).json()
        return response

    def list_deribit_contracts(self, as_of_date: str = None) -> List[dict]:
        response = requests.get(
            f'{self.rest_endpoint}deribit/list-deribit-contracts?APIKey={self.api_key}&as_of_date={as_of_date}'
        ).json()
        return response

    def list_pairs(self) -> List[str]:
        response = requests.get(f'{self.rest_endpoint}observations/pairs?APIKey={self.api_key}').json()
        return response

    def pair_quote(
            self,
            pair: str = None,
            unix_time_target: str = '',
            time_target_width: str = '') -> Optional[dict]:
        if not pair:
            print('missing "pair" parameter')
            return
        url = f'{self.rest_endpoint}observations/tick/snap?APIKey={self.api_key}&pair={pair}'
        if unix_time_target:
            url += f'&unixTimeTarget={unix_time_target}'
            url += f'&timeTargetWidthSeconds={time_target_width or 10}'
        response = requests.get(url).json()
        return response

    def pair_quote_series(
            self,
            pair: str,
            unix_time_start: Union[int, str],
            unix_time_end: Union[int, str],
            time_target_width: Union[int, str]) -> pd.DataFrame:
        number_of_periods: int = 100
        unix_time_start, unix_time_end, time_target_width = list(
            map(int, [unix_time_start, unix_time_end, time_target_width])
        )
        distance_between_periods: float = (unix_time_end - unix_time_start) / number_of_periods
        print(
            f'running time series of pair quotes with {number_of_periods}' +
            f'periods from {unix_time_start} to {unix_time_end}'
        )
        all_frames: List[dict] = []
        for i in range(number_of_periods):
            adjusted_datestamp = unix_time_start + (i * distance_between_periods)
            ith_frame = self.pair_quote(pair, f'{adjusted_datestamp}', f'{time_target_width}')
            print(f'ith_frame = {i}: {ith_frame}')
            if not len(ith_frame):
                continue
            all_frames.append(ith_frame)
        return_df = pd.DataFrame(all_frames)
        return_df['datetime'] = return_df.apply(lambda row: row['unix_time'].to_datetime())
        return return_df

    def get_options_timeslice(
            self,
            underlying_symbol: str,
            unix_time_midpoint: Union[int, str],
            width_in_seconds: Union[int, str]) -> pd.DataFrame:
        url = (
            f'{self.rest_endpoint}observations/options/time_slice?APIKey={self.api_key}&timeslice_target_datestamp='
            f'{unix_time_midpoint}&timeslice_width_seconds={width_in_seconds}'
            f'&underlying_symbol={underlying_symbol}'
        )
        return pd.DataFrame(requests.get(url).json())

    @Hybrid
    async def get_options_timeslice_series(
            self,
            underlying_symbol: str,
            unix_time_start: Union[int, str],
            unix_time_end: Union[int, str],
            time_target_width: int = 30,
            number_of_periods: int = 10) -> pd.DataFrame:
        unix_time_start, unix_time_end, time_target_width = list(
            map(int, [unix_time_start, unix_time_end, time_target_width])
        )
        period_length: float = (unix_time_end - unix_time_start) / number_of_periods
        print(
            f'running time series of pair quotes with {number_of_periods}' +
            f'periods from {unix_time_start} to {unix_time_end}'
        )
        all_frames: List[pd.DataFrame] = []
        for i in range(number_of_periods):
            adjusted_datestamp = int(unix_time_start + (i * period_length))
            ith_frame = self.get_options_timeslice(underlying_symbol, f'{adjusted_datestamp}', f'{time_target_width}')
            print(f'ith_frame = {i}: {ith_frame}')
            if not len(ith_frame):
                continue
            all_frames.append(ith_frame)
        return_df = pd.concat(all_frames)
        return return_df

    @staticmethod
    def _calc_years_to_expiry(row: dict, start_time: Union[int, str] = None) -> float:
        instrument_name = row['instrument_name']
        try:
            expiry_unix = int(dateparser.parse(instrument_name.split("-")[1]).timestamp())
        except Exception as e:
            print(f'error parsing {instrument_name.split("-")[1]} -> {e}')
            return np.nan
        years_to_expiry = (int(expiry_unix) - int(start_time or time.time())) / 60 / 60 / 24 / 365
        return years_to_expiry

    @staticmethod
    def _parse_strike_price(row: dict) -> float:
        try:
            strike_price = float(row['instrument_name'].split("-")[2])
        except ValueError:
            strike_price = np.nan
        return strike_price

    def prepare_vol_surface_inputs(
            self,
            filename: str,
            underlying_symbol: str,
            unix_time_midpoint: Union[int, str],
            width_in_seconds: Union[int, str]) -> str:
        df = self.get_options_timeslice(
            underlying_symbol,
            unix_time_midpoint,
            width_in_seconds
        )
        print('vol_surface_inputs raw:', df)
        df = df.loc[~df['underlying_index'].str.contains('SYN.')]
        df.loc[:, 'expiration'] = df.apply(lambda row: self._calc_years_to_expiry(row, unix_time_midpoint), axis=1)
        df_filtered = df.loc[df['expiration'] > 0.0]
        df_filtered.loc[:, 'strike'] = df_filtered.apply(lambda row: self._parse_strike_price(row), axis=1)
        df_filtered = df_filtered.loc[
            df_filtered['expiration'].notnull() &
            df_filtered['strike'].notnull()
        ]
        output_df = df_filtered[['expiration', 'strike', 'mark_iv']].rename(columns={"mark_iv": "price"})
        output_df.to_csv(filename, index=False)
        return filename

    @Hybrid
    async def connect(self):
        await self.__aenter__()
