"""Bitget Exchange Registry Registration."""

from __future__ import annotations

from bt_api_bitget.exchange_data import (
    BitgetExchangeDataSpot,
    BitgetExchangeDataSwap,
)
from bt_api_bitget.feeds.live_bitget import (
    BitgetAccountWssDataSpot,
    BitgetAccountWssDataSwap,
    BitgetMarketWssDataSpot,
    BitgetMarketWssDataSwap,
    BitgetRequestDataSpot,
    BitgetRequestDataSwap,
)


def _bitget_spot_subscribe_handler(data_queue, exchange_params, topics, bt_api):
    """Bitget SPOT subscription handler."""
    exchange_data = BitgetExchangeDataSpot()
    kwargs = dict(exchange_params.items())
    kwargs["wss_name"] = "bitget_market_data"
    kwargs["wss_url"] = "wss://ws.bitget.com/spot/v1/stream"
    kwargs["exchange_data"] = exchange_data
    kwargs["topics"] = topics
    BitgetMarketWssDataSpot(data_queue, **kwargs).start()
    if not bt_api._subscription_flags.get("BITGET___SPOT_account", False):
        account_kwargs = dict(kwargs.items())
        account_kwargs["topics"] = [
            {"topic": "account"},
            {"topic": "order"},
            {"topic": "trade"},
        ]
        BitgetAccountWssDataSpot(data_queue, **account_kwargs).start()
        bt_api._subscription_flags["BITGET___SPOT_account"] = True


def _bitget_swap_subscribe_handler(data_queue, exchange_params, topics, bt_api):
    """Bitget SWAP subscription handler."""
    exchange_data = BitgetExchangeDataSwap()
    kwargs = dict(exchange_params.items())
    kwargs["wss_name"] = "bitget_swap_market_data"
    kwargs["wss_url"] = "wss://ws.bitget.com/swap/v1/stream"
    kwargs["exchange_data"] = exchange_data
    kwargs["topics"] = topics
    BitgetMarketWssDataSwap(data_queue, **kwargs).start()
    if not bt_api._subscription_flags.get("BITGET___SWAP_account", False):
        account_kwargs = dict(kwargs.items())
        account_kwargs["topics"] = [
            {"topic": "account"},
            {"topic": "order"},
            {"topic": "trade"},
        ]
        BitgetAccountWssDataSwap(data_queue, **account_kwargs).start()
        bt_api._subscription_flags["BITGET___SWAP_account"] = True


def register_bitget(registry) -> None:
    """Register Bitget Spot/Swap to the provided ExchangeRegistry."""
    registry.register_feed("BITGET___SPOT", BitgetRequestDataSpot)
    registry.register_exchange_data("BITGET___SPOT", BitgetExchangeDataSpot)
    registry.register_stream("BITGET___SPOT", "subscribe", _bitget_spot_subscribe_handler)
    registry.register_feed("BITGET___SWAP", BitgetRequestDataSwap)
    registry.register_exchange_data("BITGET___SWAP", BitgetExchangeDataSwap)
    registry.register_stream("BITGET___SWAP", "subscribe", _bitget_swap_subscribe_handler)
