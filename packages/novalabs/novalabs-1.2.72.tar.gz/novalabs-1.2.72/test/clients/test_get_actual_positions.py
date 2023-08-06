from nova.clients.clients import clients
from decouple import config


def asserts_get_actual_positions(
        exchange: str,
        info: dict,
        is_exact_quantity: tuple
):

    client = clients(
        exchange=exchange,
        key=config(f"{exchange}TestAPIKey"),
        secret=config(f"{exchange}TestAPISecret"),
        passphrase=config(f"{exchange}TestPassPhrase"),
        testnet=False
    )

    # Check the current positions
    positions = client.get_actual_positions(
        pairs=list(info.keys())
    )

    if len(positions) != 0:

        for _pair, _info in positions.items():

            client.exit_market_order(
                pair=_pair,
                type_pos=_info['type_pos'],
                quantity=_info['position_size']
            )

    positions = client.get_actual_positions(
        pairs=list(info.keys())
    )

    nb_pos = 0

    assert len(positions) == nb_pos

    for pair, value in info.items():

        print(f'{value["type_pos"]} {pair} for {value["quantity"]} in position size')

        client.enter_market_order(
            pair=pair,
            type_pos=value['type_pos'],
            quantity=value["quantity"]
        )

        nb_pos += 1

        positions_ = client.get_actual_positions(pairs=info.keys())

        assert len(positions_.keys()) == nb_pos
        if is_exact_quantity[0]:
            assert positions_[pair]['position_size'] == value["quantity"]
        else:
            assert positions_[pair]['position_size'] > value["quantity"] * (1 - is_exact_quantity[1])
            assert positions_[pair]['position_size'] < value["quantity"] * (1 + is_exact_quantity[1])
        assert positions_[pair]['type_pos'] == value['type_pos']

        assert isinstance(positions_[pair]['entry_price'], float)
        assert isinstance(positions_[pair]['unrealized_pnl'], float)

    new_positions = client.get_actual_positions(
        pairs=list(info.keys())
    )

    assert len(new_positions.keys()) == len(list(info.keys()))

    for pair, _info in new_positions.items():

        client.exit_market_order(
                pair=pair,
                type_pos=_info['type_pos'],
                quantity=_info['position_size']
            )

    new_positions = client.get_actual_positions(
        pairs=list(info.keys())
    )

    assert len(new_positions) == 0

    print(f"Test get_actual_positions for {exchange.upper()} successful")


def test_get_actual_positions():

    all_tests = [
        {
            'exchange': 'binance',
            'info': {
                'BTCUSDT': {'type_pos': 'LONG', 'quantity': 0.001},
                'ETHUSDT': {'type_pos': 'SHORT', 'quantity': 0.01},
                'DOGEUSDT': {'type_pos': 'SHORT', 'quantity': 200}
            },
            'is_exact_quantity': (True, None)
        },
        # {
        #     'exchange': 'bybit',
        #     'info': {
        #         'BTCUSDT': {'type_pos': 'LONG', 'quantity': 0.001},
        #         'ETHUSDT': {'type_pos': 'SHORT', 'quantity': 0.01}
        #     },
        #     'is_exact_quantity': (True, None)
        # },
        # {
        #     'exchange': 'ftx',
        #     'info': {
        #         'BTC-PERP': {'type_pos': 'LONG', 'quantity': 0.001},
        #         'ETH-PERP': {'type_pos': 'SHORT', 'quantity': 0.01}
        #     },
        #     'is_exact_quantity': (True, None)
        # },
        {
            'exchange': 'okx',
            'info': {
                'BTC-USDT': {'type_pos': 'LONG', 'quantity': 0.001},
                'ETH-USDT': {'type_pos': 'SHORT', 'quantity': 0.01},
                'DOGE-USDT': {'type_pos': 'SHORT', 'quantity': 200}
            },
            'is_exact_quantity': (False, 0.01)
        },
        {
            'exchange': 'kucoin',
            'info': {
                'XBTUSDTM': {'type_pos': 'LONG', 'quantity': 0.001},
                'ETHUSDTM': {'type_pos': 'SHORT', 'quantity': 0.01},
                'DOGEUSDTM': {'type_pos': 'SHORT', 'quantity': 200}
            },
            'is_exact_quantity': (True, None)
        },
    ]

    for _test in all_tests:

        asserts_get_actual_positions(
            exchange=_test['exchange'],
            info=_test['info'],
            is_exact_quantity=_test['is_exact_quantity']
        )


test_get_actual_positions()
