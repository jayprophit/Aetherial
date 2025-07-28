"""
Currency Conversion Service
Provides real-time exchange rates and multi-currency support for the unified platform
"""

import asyncio
import aiohttp
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import os
from decimal import Decimal, ROUND_HALF_UP
import hashlib

class CurrencyProvider(Enum):
    EXCHANGERATE_API = "exchangerate-api"
    FIXER_IO = "fixer"
    OPEN_EXCHANGE_RATES = "openexchangerates"
    FRANKFURTER = "frankfurter"
    CURRENCY_API = "currencyapi"
    FREE_CURRENCY_API = "freecurrencyapi"

@dataclass
class ExchangeRate:
    base_currency: str
    target_currency: str
    rate: Decimal
    timestamp: datetime
    provider: str
    bid: Optional[Decimal] = None
    ask: Optional[Decimal] = None
    spread: Optional[Decimal] = None

@dataclass
class CurrencyInfo:
    code: str
    name: str
    symbol: str
    decimal_places: int = 2
    is_crypto: bool = False
    is_active: bool = True
    country_codes: List[str] = field(default_factory=list)

@dataclass
class ConversionResult:
    amount: Decimal
    from_currency: str
    to_currency: str
    converted_amount: Decimal
    exchange_rate: Decimal
    timestamp: datetime
    provider: str
    fees: Optional[Decimal] = None

class CurrencyService:
    """
    Comprehensive currency conversion service with multiple providers and caching
    """
    
    def __init__(self, data_dir: str = "./currency_data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "currency.db")
        self.cache_duration = timedelta(minutes=5)  # Cache rates for 5 minutes
        self.fallback_duration = timedelta(hours=24)  # Use fallback rates for 24 hours
        
        # API configurations
        self.providers = {
            CurrencyProvider.EXCHANGERATE_API: {
                "base_url": "https://api.exchangerate-api.com/v4/latest/",
                "free_tier": True,
                "rate_limit": 1500,  # requests per month
                "supports_historical": True
            },
            CurrencyProvider.FRANKFURTER: {
                "base_url": "https://api.frankfurter.app/",
                "free_tier": True,
                "rate_limit": None,  # No rate limit
                "supports_historical": True
            },
            CurrencyProvider.FREE_CURRENCY_API: {
                "base_url": "https://api.freecurrencyapi.com/v1/",
                "free_tier": True,
                "rate_limit": 5000,  # requests per month
                "supports_historical": True
            },
            CurrencyProvider.FIXER_IO: {
                "base_url": "http://data.fixer.io/api/",
                "free_tier": True,
                "rate_limit": 100,  # requests per month
                "supports_historical": True,
                "requires_key": True
            }
        }
        
        # Supported currencies with detailed information
        self.currencies = self._initialize_currencies()
        
        # Initialize database
        os.makedirs(data_dir, exist_ok=True)
        self._init_database()
        
        # Rate cache
        self.rate_cache: Dict[str, ExchangeRate] = {}
        self.last_cache_update = {}
        
        # Provider rotation for reliability
        self.current_provider = CurrencyProvider.FRANKFURTER
        self.provider_failures = {}
        
    def _initialize_currencies(self) -> Dict[str, CurrencyInfo]:
        """Initialize supported currencies with detailed information"""
        return {
            # Major Fiat Currencies
            "USD": CurrencyInfo("USD", "US Dollar", "$", 2, False, True, ["US"]),
            "EUR": CurrencyInfo("EUR", "Euro", "€", 2, False, True, ["DE", "FR", "IT", "ES", "NL", "BE", "AT", "PT", "IE", "GR", "FI", "LU", "SI", "CY", "MT", "SK", "EE", "LV", "LT"]),
            "GBP": CurrencyInfo("GBP", "British Pound", "£", 2, False, True, ["GB"]),
            "JPY": CurrencyInfo("JPY", "Japanese Yen", "¥", 0, False, True, ["JP"]),
            "CAD": CurrencyInfo("CAD", "Canadian Dollar", "C$", 2, False, True, ["CA"]),
            "AUD": CurrencyInfo("AUD", "Australian Dollar", "A$", 2, False, True, ["AU"]),
            "CHF": CurrencyInfo("CHF", "Swiss Franc", "CHF", 2, False, True, ["CH"]),
            "CNY": CurrencyInfo("CNY", "Chinese Yuan", "¥", 2, False, True, ["CN"]),
            "SEK": CurrencyInfo("SEK", "Swedish Krona", "kr", 2, False, True, ["SE"]),
            "NOK": CurrencyInfo("NOK", "Norwegian Krone", "kr", 2, False, True, ["NO"]),
            "MXN": CurrencyInfo("MXN", "Mexican Peso", "$", 2, False, True, ["MX"]),
            "SGD": CurrencyInfo("SGD", "Singapore Dollar", "S$", 2, False, True, ["SG"]),
            "HKD": CurrencyInfo("HKD", "Hong Kong Dollar", "HK$", 2, False, True, ["HK"]),
            "NZD": CurrencyInfo("NZD", "New Zealand Dollar", "NZ$", 2, False, True, ["NZ"]),
            "KRW": CurrencyInfo("KRW", "South Korean Won", "₩", 0, False, True, ["KR"]),
            "TRY": CurrencyInfo("TRY", "Turkish Lira", "₺", 2, False, True, ["TR"]),
            "RUB": CurrencyInfo("RUB", "Russian Ruble", "₽", 2, False, True, ["RU"]),
            "INR": CurrencyInfo("INR", "Indian Rupee", "₹", 2, False, True, ["IN"]),
            "BRL": CurrencyInfo("BRL", "Brazilian Real", "R$", 2, False, True, ["BR"]),
            "ZAR": CurrencyInfo("ZAR", "South African Rand", "R", 2, False, True, ["ZA"]),
            
            # Middle East & Africa
            "AED": CurrencyInfo("AED", "UAE Dirham", "د.إ", 2, False, True, ["AE"]),
            "SAR": CurrencyInfo("SAR", "Saudi Riyal", "﷼", 2, False, True, ["SA"]),
            "EGP": CurrencyInfo("EGP", "Egyptian Pound", "£", 2, False, True, ["EG"]),
            "NGN": CurrencyInfo("NGN", "Nigerian Naira", "₦", 2, False, True, ["NG"]),
            
            # Asia Pacific
            "THB": CurrencyInfo("THB", "Thai Baht", "฿", 2, False, True, ["TH"]),
            "MYR": CurrencyInfo("MYR", "Malaysian Ringgit", "RM", 2, False, True, ["MY"]),
            "IDR": CurrencyInfo("IDR", "Indonesian Rupiah", "Rp", 0, False, True, ["ID"]),
            "PHP": CurrencyInfo("PHP", "Philippine Peso", "₱", 2, False, True, ["PH"]),
            "VND": CurrencyInfo("VND", "Vietnamese Dong", "₫", 0, False, True, ["VN"]),
            
            # Latin America
            "ARS": CurrencyInfo("ARS", "Argentine Peso", "$", 2, False, True, ["AR"]),
            "CLP": CurrencyInfo("CLP", "Chilean Peso", "$", 0, False, True, ["CL"]),
            "COP": CurrencyInfo("COP", "Colombian Peso", "$", 0, False, True, ["CO"]),
            "PEN": CurrencyInfo("PEN", "Peruvian Sol", "S/", 2, False, True, ["PE"]),
            
            # Cryptocurrencies
            "BTC": CurrencyInfo("BTC", "Bitcoin", "₿", 8, True, True, []),
            "ETH": CurrencyInfo("ETH", "Ethereum", "Ξ", 8, True, True, []),
            "USDT": CurrencyInfo("USDT", "Tether", "₮", 6, True, True, []),
            "BNB": CurrencyInfo("BNB", "Binance Coin", "BNB", 8, True, True, []),
            "ADA": CurrencyInfo("ADA", "Cardano", "₳", 6, True, True, []),
            "DOT": CurrencyInfo("DOT", "Polkadot", "DOT", 6, True, True, []),
            "LINK": CurrencyInfo("LINK", "Chainlink", "LINK", 6, True, True, []),
            "LTC": CurrencyInfo("LTC", "Litecoin", "Ł", 8, True, True, []),
            "BCH": CurrencyInfo("BCH", "Bitcoin Cash", "BCH", 8, True, True, []),
            "XRP": CurrencyInfo("XRP", "Ripple", "XRP", 6, True, True, []),
        }
    
    def _init_database(self):
        """Initialize SQLite database for caching rates and historical data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Exchange rates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base_currency TEXT NOT NULL,
                target_currency TEXT NOT NULL,
                rate DECIMAL(20, 10) NOT NULL,
                timestamp DATETIME NOT NULL,
                provider TEXT NOT NULL,
                bid DECIMAL(20, 10),
                ask DECIMAL(20, 10),
                spread DECIMAL(20, 10),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(base_currency, target_currency, provider, timestamp)
            )
        ''')
        
        # Currency preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_currency_preferences (
                user_id TEXT PRIMARY KEY,
                preferred_currency TEXT NOT NULL,
                display_format TEXT DEFAULT 'symbol',
                auto_detect_location BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Conversion history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversion_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                amount DECIMAL(20, 10) NOT NULL,
                from_currency TEXT NOT NULL,
                to_currency TEXT NOT NULL,
                converted_amount DECIMAL(20, 10) NOT NULL,
                exchange_rate DECIMAL(20, 10) NOT NULL,
                provider TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rates_currencies ON exchange_rates(base_currency, target_currency)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rates_timestamp ON exchange_rates(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversion_user ON conversion_history(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversion_timestamp ON conversion_history(timestamp)')
        
        conn.commit()
        conn.close()
    
    async def get_exchange_rate(self, from_currency: str, to_currency: str, 
                              force_refresh: bool = False) -> Optional[ExchangeRate]:
        """Get exchange rate between two currencies"""
        try:
            # Normalize currency codes
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            
            # Same currency
            if from_currency == to_currency:
                return ExchangeRate(
                    base_currency=from_currency,
                    target_currency=to_currency,
                    rate=Decimal('1.0'),
                    timestamp=datetime.utcnow(),
                    provider="internal"
                )
            
            # Check cache first
            cache_key = f"{from_currency}_{to_currency}"
            if not force_refresh and cache_key in self.rate_cache:
                cached_rate = self.rate_cache[cache_key]
                if datetime.utcnow() - cached_rate.timestamp < self.cache_duration:
                    return cached_rate
            
            # Try to get fresh rate from API
            rate = await self._fetch_rate_from_api(from_currency, to_currency)
            
            if rate:
                # Cache the rate
                self.rate_cache[cache_key] = rate
                
                # Store in database
                await self._store_rate_in_db(rate)
                
                return rate
            
            # Fallback to database
            return await self._get_rate_from_db(from_currency, to_currency)
            
        except Exception as e:
            logging.error(f"Error getting exchange rate {from_currency} to {to_currency}: {e}")
            return await self._get_rate_from_db(from_currency, to_currency)
    
    async def _fetch_rate_from_api(self, from_currency: str, to_currency: str) -> Optional[ExchangeRate]:
        """Fetch exchange rate from external API"""
        providers_to_try = [self.current_provider] + [p for p in CurrencyProvider if p != self.current_provider]
        
        for provider in providers_to_try:
            try:
                rate = await self._fetch_from_provider(provider, from_currency, to_currency)
                if rate:
                    self.current_provider = provider  # Update current provider on success
                    self.provider_failures.pop(provider, None)  # Clear failure count
                    return rate
            except Exception as e:
                logging.warning(f"Provider {provider.value} failed: {e}")
                self.provider_failures[provider] = self.provider_failures.get(provider, 0) + 1
                continue
        
        return None
    
    async def _fetch_from_provider(self, provider: CurrencyProvider, 
                                 from_currency: str, to_currency: str) -> Optional[ExchangeRate]:
        """Fetch rate from specific provider"""
        config = self.providers[provider]
        
        async with aiohttp.ClientSession() as session:
            if provider == CurrencyProvider.FRANKFURTER:
                url = f"{config['base_url']}latest?from={from_currency}&to={to_currency}"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'rates' in data and to_currency in data['rates']:
                            return ExchangeRate(
                                base_currency=from_currency,
                                target_currency=to_currency,
                                rate=Decimal(str(data['rates'][to_currency])),
                                timestamp=datetime.utcnow(),
                                provider=provider.value
                            )
            
            elif provider == CurrencyProvider.EXCHANGERATE_API:
                url = f"{config['base_url']}{from_currency}"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'rates' in data and to_currency in data['rates']:
                            return ExchangeRate(
                                base_currency=from_currency,
                                target_currency=to_currency,
                                rate=Decimal(str(data['rates'][to_currency])),
                                timestamp=datetime.utcnow(),
                                provider=provider.value
                            )
            
            elif provider == CurrencyProvider.FREE_CURRENCY_API:
                url = f"{config['base_url']}latest?apikey=fca_live_YOUR_API_KEY&currencies={to_currency}&base_currency={from_currency}"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'data' in data and to_currency in data['data']:
                            return ExchangeRate(
                                base_currency=from_currency,
                                target_currency=to_currency,
                                rate=Decimal(str(data['data'][to_currency])),
                                timestamp=datetime.utcnow(),
                                provider=provider.value
                            )
        
        return None
    
    async def _store_rate_in_db(self, rate: ExchangeRate):
        """Store exchange rate in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            
(Content truncated due to size limit. Use line ranges to read in chunks)