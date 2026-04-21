# bt_api_bitget

Bitget exchange package for `bt_api`, supporting Spot and USDT-M Perpetual swap trading.

## Features

- **Spot Trading**: Full REST API support for account, orders, market data
- **USDT-M Swap**: REST API for perpetual futures trading
- **HMAC SHA256 + Base64 Authentication**: Secure API key handling
- **Hardcoded Configuration**: No YAML dependency — all exchange paths and kline periods are defined in code

## Installation

```bash
pip install bt_api_bitget
```

Or install from source:

```bash
cd packages/bt_api_bitget
pip install -e .
```

## Quick Usage

```python
from bt_api_py import BtApi

api = BtApi(
    exchange_kwargs={
        "BITGET___SPOT": {
            "api_key": "your_api_key",
            "secret_key": "your_secret",
            "passphrase": "your_passphrase",
        }
    }
)

# Query ticker
ticker = api.get_tick("BITGET___SPOT", "BTCUSDT")
print(ticker)

# Place order
order = api.make_order(
    exchange_name="BITGET___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="buy-limit",
)
print(order)
```

## Architecture

```
bt_api_bitget/
├── __init__.py
├── exchange_data/
│   └── __init__.py          # BitgetExchangeData, BitgetExchangeDataSpot, BitgetExchangeDataSwap
├── errors/
│   ├── __init__.py           # BitgetErrorTranslator (re-export)
│   └── bitget_translator.py  # Error code mapping
├── containers/
│   ├── __init__.py
│   ├── balances/
│   │   ├── __init__.py
│   │   └── bitget_balance.py  # BalanceData, WssBalanceData, RequestBalanceData
│   ├── orders/
│   │   ├── __init__.py
│   │   └── bitget_order.py    # OrderData, WssOrderData, RequestOrderData
│   ├── tickers/
│   │   ├── __init__.py
│   │   └── bitget_ticker.py   # TickerData, WssTickerData, RequestTickerData
│   └── orderbooks/
│       ├── __init__.py
│       └── bitget_orderbook.py # OrderBookData, WssOrderBookData, RequestOrderBookData
├── feeds/
│   └── live_bitget/
│       ├── __init__.py
│       ├── request_base.py    # BitgetRequestData (HMAC auth base)
│       ├── spot.py            # BitgetRequestDataSpot + WSS placeholders
│       └── swap.py            # BitgetRequestDataSwap + WSS placeholders
├── registry_registration.py   # Auto-registers with ExchangeRegistry
└── plugin.py                  # Plugin entrypoint for unified loading
```

## Dependencies

- `bt_api_base>=0.15,<1.0`
- Python 3.9+

## Supported Endpoints

### Spot

| Method | Description |
|--------|-------------|
| `get_ticker` / `get_tick` | Query ticker data |
| `get_depth` / `get_orderbook` | Order book depth |
| `get_kline` / `get_klines` | K-line/candlestick data |
| `get_server_time` | Server time |
| `get_exchange_info` / `get_symbols` | Exchange symbols |
| `get_balance` | Account balances |
| `get_account` | Account info |
| `make_order` | Place order |
| `cancel_order` | Cancel order |
| `query_order` | Query order status |
| `get_deals` | Recent trades |

### Swap (USDT-M)

Same as Spot with swap-specific endpoints including `get_funding_rate`, `get_position`, `change_leverage`.

## WebSocket

WebSocket classes (`BitgetMarketWssDataSpot`, `BitgetAccountWssDataSpot`, etc.) are placeholder stubs. Full WebSocket implementation is pending.

## Error Codes

`BitgetErrorTranslator` maps Bitget API error messages to unified `UnifiedErrorCode` values from `bt_api_base.error`.
