"""
Currency Manager - Multi-currency support
"""

from loguru import logger
from typing import Dict, Optional
from datetime import datetime


class CurrencyManager:
    """Manages currency conversion and exchange rates"""
    
    # Default exchange rates (can be updated from API)
    DEFAULT_RATES = {
        'USD': 1.0,
        'EUR': 0.85,
        'GBP': 0.73,
        'JPY': 110.0,
        'CAD': 1.25,
        'AUD': 1.35,
        'CHF': 0.92,
        'CNY': 6.45,
        'INR': 74.0,
        'MXN': 20.0,
    }
    
    def __init__(self):
        self.exchange_rates = self.DEFAULT_RATES.copy()
        self.base_currency = 'USD'
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Get exchange rate between two currencies
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            Exchange rate (amount in to_currency per 1 from_currency)
        """
        if from_currency == to_currency:
            return 1.0
        
        from_rate = self.exchange_rates.get(from_currency.upper(), 1.0)
        to_rate = self.exchange_rates.get(to_currency.upper(), 1.0)
        
        # Convert via base currency (USD)
        if from_currency.upper() == self.base_currency:
            return to_rate
        elif to_currency.upper() == self.base_currency:
            return 1.0 / from_rate
        else:
            # Convert from -> USD -> to
            return to_rate / from_rate
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert amount from one currency to another
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            Converted amount
        """
        rate = self.get_exchange_rate(from_currency, to_currency)
        return amount * rate
    
    def format_currency(self, amount: float, currency: str) -> str:
        """
        Format amount with currency symbol
        
        Args:
            amount: Amount to format
            currency: Currency code
            
        Returns:
            Formatted string (e.g., "$100.00" or "€85.00")
        """
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CAD': 'C$',
            'AUD': 'A$',
            'CHF': 'CHF',
            'CNY': '¥',
            'INR': '₹',
            'MXN': '$',
        }
        
        symbol = currency_symbols.get(currency.upper(), currency.upper())
        return f"{symbol}{amount:,.2f}"
    
    def update_exchange_rate(self, currency: str, rate: float):
        """
        Update exchange rate for a currency (relative to base currency)
        
        Args:
            currency: Currency code
            rate: Exchange rate (amount in currency per 1 base currency)
        """
        self.exchange_rates[currency.upper()] = rate
        logger.info(f"Updated exchange rate for {currency}: {rate}")
    
    def get_supported_currencies(self) -> list:
        """Get list of supported currency codes"""
        return list(self.exchange_rates.keys())
    
    def set_base_currency(self, currency: str):
        """
        Set base currency (all rates are relative to this)
        
        Args:
            currency: Currency code to set as base
        """
        if currency.upper() in self.exchange_rates:
            # Convert all rates to new base
            old_base_rate = self.exchange_rates.get(currency.upper(), 1.0)
            for curr in self.exchange_rates:
                if curr != currency.upper():
                    self.exchange_rates[curr] = self.exchange_rates[curr] / old_base_rate
            self.exchange_rates[currency.upper()] = 1.0
            self.base_currency = currency.upper()
            logger.info(f"Base currency set to: {currency}")


# Global instance
_currency_manager = None


def get_currency_manager() -> CurrencyManager:
    """Get global currency manager instance"""
    global _currency_manager
    if _currency_manager is None:
        _currency_manager = CurrencyManager()
    return _currency_manager

