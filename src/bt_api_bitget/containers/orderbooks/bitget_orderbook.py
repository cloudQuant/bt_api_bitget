"""Bitget OrderBook Data Container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.orderbooks.orderbook import OrderBookData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_int, from_dict_get_string


class BitgetOrderBookData(OrderBookData):
    """Bitget order book data container.

    Holds and manages order book information from Bitget exchange,
    including bid and ask lists and related calculations.
    """

    def __init__(
        self,
        orderbook_info: str | dict,
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """Initialize Bitget order book data.

        Args:
            orderbook_info: Raw order book data (JSON string or dict)
            symbol_name: Trading pair name
            asset_type: Asset type (e.g., 'SPOT', 'SWAP')
            has_been_json_encoded: Whether data is already JSON encoded
        """
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "BITGET"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.orderbook_data: Any = orderbook_info if has_been_json_encoded else None
        self.symbol: str | None = None
        self.time: float | None = None
        self.bids: list[tuple[float, float]] = []
        self.asks: list[tuple[float, float]] = []
        self.level: int | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> BitgetOrderBookData:
        """Initialize and parse order book data."""
        if not self.has_been_json_encoded:
            self.orderbook_data = json.loads(self.order_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        self.symbol = from_dict_get_string(self.orderbook_data, "symbol")
        self.time = from_dict_get_float(self.orderbook_data, "ts") or from_dict_get_float(
            self.orderbook_data, "time"
        )
        self.level = from_dict_get_int(self.orderbook_data, "level")

        self.bids = []
        if "bids" in self.orderbook_data:
            for bid in self.orderbook_data["bids"]:
                if isinstance(bid, list) and len(bid) >= 2:
                    self.bids.append((float(bid[0]), float(bid[1])))

        self.asks = []
        if "asks" in self.orderbook_data:
            for ask in self.orderbook_data["asks"]:
                if isinstance(ask, list) and len(ask) >= 2:
                    self.asks.append((float(ask[0]), float(ask[1])))

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        """Get all order book data."""
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "symbol": self.symbol,
                "time": self.time,
                "level": self.level,
                "bids": self.bids,
                "asks": self.asks,
            }
        return self.all_data

    def __str__(self) -> str:
        """Return JSON string representation."""
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        """Return string representation."""
        return self.__str__()

    def get_exchange_name(self) -> str:
        """Get exchange name."""
        return self.exchange_name

    def get_local_update_time(self) -> float:
        """Get local update timestamp."""
        return self.local_update_time

    def get_symbol_name(self) -> str:
        """Get trading pair name."""
        return self.symbol_name

    def get_asset_type(self) -> str:
        """Get asset type."""
        return self.asset_type

    def get_symbol(self) -> str | None:
        """Get exchange raw trading pair symbol."""
        return self.symbol

    def get_time(self) -> float | None:
        """Get server timestamp."""
        return self.time

    def get_level(self) -> int | None:
        """Get order book depth level."""
        return self.level

    def get_bids(self) -> list[tuple[float, float]]:
        """Get bid list (sorted by price descending)."""
        self.init_data()
        return sorted(self.bids, key=lambda x: x[0], reverse=True)

    def get_asks(self) -> list[tuple[float, float]]:
        """Get ask list (sorted by price ascending)."""
        self.init_data()
        return sorted(self.asks, key=lambda x: x[0])

    def get_spread(self) -> float | None:
        """Get bid-ask spread."""
        self.init_data()
        if not self.bids or not self.asks:
            return None
        best_bid = max(bid[0] for bid in self.bids)
        best_ask = min(ask[0] for ask in self.asks)
        return best_ask - best_bid

    def get_best_bid(self) -> float | None:
        """Get best bid price."""
        self.init_data()
        if not self.bids:
            return None
        return max(bid[0] for bid in self.bids)

    def get_best_ask(self) -> float | None:
        """Get best ask price."""
        self.init_data()
        if not self.asks:
            return None
        return min(ask[0] for ask in self.asks)

    def get_total_bid_volume(self) -> float:
        """Get total bid volume."""
        self.init_data()
        return sum(bid[1] for bid in self.bids)

    def get_total_ask_volume(self) -> float:
        """Get total ask volume."""
        self.init_data()
        return sum(ask[1] for ask in self.asks)

    def get_mid_price(self) -> float | None:
        """Get mid price (average of best bid and best ask)."""
        self.init_data()
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        if best_bid is None or best_ask is None:
            return None
        return (best_bid + best_ask) / 2


class BitgetWssOrderBookData(BitgetOrderBookData):
    """Bitget WebSocket order book data container."""

    def init_data(self) -> BitgetWssOrderBookData:
        """Initialize and parse WebSocket order book data."""
        if not self.has_been_json_encoded:
            self.orderbook_data = json.loads(self.order_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        self.symbol = from_dict_get_string(self.orderbook_data, "s")
        self.time = from_dict_get_float(self.orderbook_data, "E")
        self.level = 1

        self.bids = []
        if "b" in self.orderbook_data:
            for bid in self.orderbook_data["b"]:
                if isinstance(bid, list) and len(bid) >= 2:
                    self.bids.append((float(bid[0]), float(bid[1])))

        self.asks = []
        if "a" in self.orderbook_data:
            for ask in self.orderbook_data["a"]:
                if isinstance(ask, list) and len(ask) >= 2:
                    self.asks.append((float(ask[0]), float(ask[1])))

        self.has_been_init_data = True
        return self


class BitgetRequestOrderBookData(BitgetOrderBookData):
    """Bitget REST API order book data container."""

    def init_data(self) -> BitgetRequestOrderBookData:
        """Initialize and parse REST API order book data."""
        if not self.has_been_json_encoded:
            self.orderbook_data = json.loads(self.order_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        self.symbol = from_dict_get_string(self.orderbook_data, "symbol")
        self.time = from_dict_get_float(self.orderbook_data, "ts")
        self.level = from_dict_get_int(self.orderbook_data, "level")

        self.bids = []
        if "bids" in self.orderbook_data:
            for bid in self.orderbook_data["bids"]:
                if isinstance(bid, list) and len(bid) >= 2:
                    self.bids.append((float(bid[0]), float(bid[1])))

        self.asks = []
        if "asks" in self.orderbook_data:
            for ask in self.orderbook_data["asks"]:
                if isinstance(ask, list) and len(ask) >= 2:
                    self.asks.append((float(ask[0]), float(ask[1])))

        self.has_been_init_data = True
        return self
