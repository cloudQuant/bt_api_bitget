"""Tests for BitgetExchangeData container."""

from __future__ import annotations

from bt_api_bitget.exchange_data import BitgetExchangeData


class TestBitgetExchangeData:
    """Tests for BitgetExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = BitgetExchangeData()

        assert exchange.exchange_name == "BITGET"
