import time
import asyncio
from datetime import timedelta, datetime
from nova.clients.clients import clients
from decouple import config


def asserts_get_prod_data(
        exchange: str,
        list_pair: list,
        nb_candles: int,
        testnet: bool
):

    client = clients(
        exchange=exchange,
        key=config(f"{exchange}TestAPIKey"),
        secret=config(f"{exchange}TestAPISecret"),
        passphrase=config(f"{exchange}TestPassPhrase"),
        testnet=testnet
    )

    print('First Fetching Data')
    client.prod_data = asyncio.run(client.get_prod_data(
        list_pair=list_pair,
        interval='1m',
        nb_candles=nb_candles,
        current_state=None
    ))

    assert list(client.prod_data.keys()) == list_pair

    for _pair in list_pair:
        data = client.prod_data[_pair]['data']
        data['time_dif'] = data['open_time'] - data['open_time'].shift(1)

        assert str(client.prod_data[_pair]['data'].dtypes['open_time']) == 'datetime64[ns]'
        assert str(client.prod_data[_pair]['data'].dtypes['close_time']) == 'datetime64[ns]'

        assert data['time_dif'].min() == timedelta(minutes=1), f'Wrong incrementation'
        assert data['time_dif'].max() == timedelta(minutes=1), f'Wrong incrementation'

    print(f'Testing Updates on the production data for 2 minutes')

    idx = 0
    while idx < 3:

        if datetime.now().second == 0:

            t_verify = datetime.utcfromtimestamp(time.time())

            print(f"----- {t_verify} -----")

            print('Update Production Data')

            client.prod_data = asyncio.run(client.get_prod_data(
                list_pair=list_pair,
                interval='1m',
                nb_candles=nb_candles,
                current_state=client.prod_data
            ))

            t_last_open = t_verify - timedelta(
                microseconds=t_verify.microsecond,
                seconds=t_verify.second
            ) - timedelta(minutes=1)

            for pair in client.prod_data.keys():

                data = client.prod_data[pair]['data']

                data['time_dif'] = data['open_time'] - data['open_time'].shift(1)

                assert len(data) == nb_candles, f'DataFrame has the wrong size. {pair}'
                assert data['time_dif'].min() == timedelta(minutes=1), f'Missing row in the DataFrame. {pair}'
                assert data['time_dif'].max() == timedelta(minutes=1), f'Missing row in the DataFrame. {pair}'
                assert (data['open_time'] == t_last_open).values[-1], f'Wrong last candle. {pair}'

            print('All tests passed')
            idx += 1
            time.sleep(1)

    print(f"Test get_prod_data for {exchange.upper()} successful")


def test_get_prod_data():

    all_tests = [
        {
            'exchange': 'binance',
            'list_pair': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'TLMUSDT', 'DOGEUSDT', 'LTCUSDT', 'ETCUSDT'],
            'nb_candles': 400,
            'testnet': False
        },
        {
            'exchange': 'bybit',
            'list_pair': ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT', 'GMTUSDT', 'SANDUSDT',
                          'APEUSDT', 'LTCUSDT', 'AVAXUSDT', 'SHIB1000USDT', 'MATICUSDT', 'DOGEUSDT', 'DOTUSDT',
                          'ETCUSDT', 'NEARUSDT', 'LINKUSDT', 'GALAUSDT', 'XTZUSDT', 'AXSUSDT'],
            'nb_candles': 400,
            'testnet': False
        },
        {
            'exchange': 'ftx',
            'list_pair': ['BTC-PERP', 'ETH-PERP', 'XRP-PERP', 'FTT-PERP', 'SOL-PERP'],
            'nb_candles': 400,
            'testnet': False
        },
        {
            'exchange': 'okx',
            'list_pair': ['ETH-USDT', 'BTC-USDT', 'ADA-USDT', 'SOL-USDT', 'DOGE-USDT'],
            'nb_candles': 300,
            'testnet': False
        },
        {
            'exchange': 'kucoin',
            'list_pair': ['XBTUSDTM', 'ETHUSDTM', 'LINKUSDTM', 'SOLUSDTM'],
            'nb_candles': 300,
            'testnet': False
        },
        {
            'exchange': 'oanda',
            'list_pair': ['EUR_USD', 'AUD_NZD', 'EUR_JPY'],
            'nb_candles': 400,
            'testnet': True
        },
    ]

    for _test in all_tests:

        asserts_get_prod_data(
            exchange=_test['exchange'],
            list_pair=_test['list_pair'],
            nb_candles=_test['nb_candles'],
            testnet=_test['testnet']
        )


test_get_prod_data()
