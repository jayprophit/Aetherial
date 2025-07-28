import React, { useState, useEffect } from 'react';

interface Currency {
  code: string;
  name: string;
  symbol: string;
  flag: string;
  type: 'fiat' | 'crypto';
}

interface ExchangeRate {
  from: string;
  to: string;
  rate: number;
  lastUpdated: string;
}

const CurrencyConverter: React.FC = () => {
  const [amount, setAmount] = useState<string>('1');
  const [fromCurrency, setFromCurrency] = useState<string>('USD');
  const [toCurrency, setToCurrency] = useState<string>('EUR');
  const [convertedAmount, setConvertedAmount] = useState<string>('0');
  const [exchangeRate, setExchangeRate] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [lastUpdated, setLastUpdated] = useState<string>('');

  // Comprehensive currency list including fiat and crypto
  const currencies: Currency[] = [
    // Major Fiat Currencies
    { code: 'USD', name: 'US Dollar', symbol: '$', flag: '🇺🇸', type: 'fiat' },
    { code: 'EUR', name: 'Euro', symbol: '€', flag: '🇪🇺', type: 'fiat' },
    { code: 'GBP', name: 'British Pound', symbol: '£', flag: '🇬🇧', type: 'fiat' },
    { code: 'JPY', name: 'Japanese Yen', symbol: '¥', flag: '🇯🇵', type: 'fiat' },
    { code: 'CHF', name: 'Swiss Franc', symbol: 'CHF', flag: '🇨🇭', type: 'fiat' },
    { code: 'CAD', name: 'Canadian Dollar', symbol: 'C$', flag: '🇨🇦', type: 'fiat' },
    { code: 'AUD', name: 'Australian Dollar', symbol: 'A$', flag: '🇦🇺', type: 'fiat' },
    { code: 'NZD', name: 'New Zealand Dollar', symbol: 'NZ$', flag: '🇳🇿', type: 'fiat' },
    { code: 'CNY', name: 'Chinese Yuan', symbol: '¥', flag: '🇨🇳', type: 'fiat' },
    { code: 'INR', name: 'Indian Rupee', symbol: '₹', flag: '🇮🇳', type: 'fiat' },
    { code: 'KRW', name: 'South Korean Won', symbol: '₩', flag: '🇰🇷', type: 'fiat' },
    { code: 'SGD', name: 'Singapore Dollar', symbol: 'S$', flag: '🇸🇬', type: 'fiat' },
    { code: 'HKD', name: 'Hong Kong Dollar', symbol: 'HK$', flag: '🇭🇰', type: 'fiat' },
    { code: 'NOK', name: 'Norwegian Krone', symbol: 'kr', flag: '🇳🇴', type: 'fiat' },
    { code: 'SEK', name: 'Swedish Krona', symbol: 'kr', flag: '🇸🇪', type: 'fiat' },
    { code: 'DKK', name: 'Danish Krone', symbol: 'kr', flag: '🇩🇰', type: 'fiat' },
    { code: 'PLN', name: 'Polish Zloty', symbol: 'zł', flag: '🇵🇱', type: 'fiat' },
    { code: 'CZK', name: 'Czech Koruna', symbol: 'Kč', flag: '🇨🇿', type: 'fiat' },
    { code: 'HUF', name: 'Hungarian Forint', symbol: 'Ft', flag: '🇭🇺', type: 'fiat' },
    { code: 'RUB', name: 'Russian Ruble', symbol: '₽', flag: '🇷🇺', type: 'fiat' },
    { code: 'BRL', name: 'Brazilian Real', symbol: 'R$', flag: '🇧🇷', type: 'fiat' },
    { code: 'MXN', name: 'Mexican Peso', symbol: '$', flag: '🇲🇽', type: 'fiat' },
    { code: 'ARS', name: 'Argentine Peso', symbol: '$', flag: '🇦🇷', type: 'fiat' },
    { code: 'CLP', name: 'Chilean Peso', symbol: '$', flag: '🇨🇱', type: 'fiat' },
    { code: 'COP', name: 'Colombian Peso', symbol: '$', flag: '🇨🇴', type: 'fiat' },
    { code: 'ZAR', name: 'South African Rand', symbol: 'R', flag: '🇿🇦', type: 'fiat' },
    { code: 'TRY', name: 'Turkish Lira', symbol: '₺', flag: '🇹🇷', type: 'fiat' },
    { code: 'ILS', name: 'Israeli Shekel', symbol: '₪', flag: '🇮🇱', type: 'fiat' },
    { code: 'AED', name: 'UAE Dirham', symbol: 'د.إ', flag: '🇦🇪', type: 'fiat' },
    { code: 'SAR', name: 'Saudi Riyal', symbol: '﷼', flag: '🇸🇦', type: 'fiat' },
    { code: 'EGP', name: 'Egyptian Pound', symbol: '£', flag: '🇪🇬', type: 'fiat' },
    { code: 'NGN', name: 'Nigerian Naira', symbol: '₦', flag: '🇳🇬', type: 'fiat' },
    { code: 'KES', name: 'Kenyan Shilling', symbol: 'KSh', flag: '🇰🇪', type: 'fiat' },
    { code: 'GHS', name: 'Ghanaian Cedi', symbol: '₵', flag: '🇬🇭', type: 'fiat' },
    { code: 'THB', name: 'Thai Baht', symbol: '฿', flag: '🇹🇭', type: 'fiat' },
    { code: 'VND', name: 'Vietnamese Dong', symbol: '₫', flag: '🇻🇳', type: 'fiat' },
    { code: 'IDR', name: 'Indonesian Rupiah', symbol: 'Rp', flag: '🇮🇩', type: 'fiat' },
    { code: 'MYR', name: 'Malaysian Ringgit', symbol: 'RM', flag: '🇲🇾', type: 'fiat' },
    { code: 'PHP', name: 'Philippine Peso', symbol: '₱', flag: '🇵🇭', type: 'fiat' },

    // Major Cryptocurrencies
    { code: 'BTC', name: 'Bitcoin', symbol: '₿', flag: '🟠', type: 'crypto' },
    { code: 'ETH', name: 'Ethereum', symbol: 'Ξ', flag: '🔷', type: 'crypto' },
    { code: 'BNB', name: 'Binance Coin', symbol: 'BNB', flag: '🟡', type: 'crypto' },
    { code: 'XRP', name: 'Ripple', symbol: 'XRP', flag: '🔵', type: 'crypto' },
    { code: 'ADA', name: 'Cardano', symbol: 'ADA', flag: '🔵', type: 'crypto' },
    { code: 'DOGE', name: 'Dogecoin', symbol: 'Ð', flag: '🟡', type: 'crypto' },
    { code: 'SOL', name: 'Solana', symbol: 'SOL', flag: '🟣', type: 'crypto' },
    { code: 'DOT', name: 'Polkadot', symbol: 'DOT', flag: '🔴', type: 'crypto' },
    { code: 'MATIC', name: 'Polygon', symbol: 'MATIC', flag: '🟣', type: 'crypto' },
    { code: 'SHIB', name: 'Shiba Inu', symbol: 'SHIB', flag: '🟠', type: 'crypto' },
    { code: 'AVAX', name: 'Avalanche', symbol: 'AVAX', flag: '🔴', type: 'crypto' },
    { code: 'UNI', name: 'Uniswap', symbol: 'UNI', flag: '🦄', type: 'crypto' },
    { code: 'LINK', name: 'Chainlink', symbol: 'LINK', flag: '🔵', type: 'crypto' },
    { code: 'LTC', name: 'Litecoin', symbol: 'Ł', flag: '⚪', type: 'crypto' },
    { code: 'BCH', name: 'Bitcoin Cash', symbol: 'BCH', flag: '🟢', type: 'crypto' },
    { code: 'ALGO', name: 'Algorand', symbol: 'ALGO', flag: '⚫', type: 'crypto' },
    { code: 'XLM', name: 'Stellar', symbol: 'XLM', flag: '⚪', type: 'crypto' },
    { code: 'VET', name: 'VeChain', symbol: 'VET', flag: '🔵', type: 'crypto' },
    { code: 'ICP', name: 'Internet Computer', symbol: 'ICP', flag: '🟣', type: 'crypto' },
    { code: 'FIL', name: 'Filecoin', symbol: 'FIL', flag: '🔵', type: 'crypto' },
    { code: 'TRX', name: 'TRON', symbol: 'TRX', flag: '🔴', type: 'crypto' },
    { code: 'ETC', name: 'Ethereum Classic', symbol: 'ETC', flag: '🟢', type: 'crypto' },
    { code: 'XMR', name: 'Monero', symbol: 'XMR', flag: '🟠', type: 'crypto' },
    { code: 'THETA', name: 'Theta Network', symbol: 'THETA', flag: '🔵', type: 'crypto' },
    { code: 'AAVE', name: 'Aave', symbol: 'AAVE', flag: '🟣', type: 'crypto' },
    { code: 'MKR', name: 'Maker', symbol: 'MKR', flag: '🟢', type: 'crypto' },
    { code: 'COMP', name: 'Compound', symbol: 'COMP', flag: '🟢', type: 'crypto' },
    { code: 'SUSHI', name: 'SushiSwap', symbol: 'SUSHI', flag: '🍣', type: 'crypto' },
    { code: 'CRV', name: 'Curve DAO Token', symbol: 'CRV', flag: '🔵', type: 'crypto' },
    { code: 'YFI', name: 'yearn.finance', symbol: 'YFI', flag: '🔵', type: 'crypto' },

    // Stablecoins
    { code: 'USDT', name: 'Tether', symbol: 'USDT', flag: '🟢', type: 'crypto' },
    { code: 'USDC', name: 'USD Coin', symbol: 'USDC', flag: '🔵', type: 'crypto' },
    { code: 'BUSD', name: 'Binance USD', symbol: 'BUSD', flag: '🟡', type: 'crypto' },
    { code: 'DAI', name: 'Dai', symbol: 'DAI', flag: '🟡', type: 'crypto' },
    { code: 'TUSD', name: 'TrueUSD', symbol: 'TUSD', flag: '🔵', type: 'crypto' },
    { code: 'USDP', name: 'Pax Dollar', symbol: 'USDP', flag: '🟢', type: 'crypto' },
  ];

  // Mock exchange rates (in production, this would come from a real API)
  const mockExchangeRates: { [key: string]: number } = {
    'USD-EUR': 0.85,
    'USD-GBP': 0.73,
    'USD-JPY': 110.0,
    'USD-CHF': 0.92,
    'USD-CAD': 1.25,
    'USD-AUD': 1.35,
    'USD-CNY': 6.45,
    'USD-INR': 74.5,
    'USD-BTC': 0.000023,
    'USD-ETH': 0.00027,
    'USD-BNB': 0.0017,
    'BTC-USD': 43500,
    'ETH-USD': 3200,
    'BNB-USD': 580,
    'EUR-USD': 1.18,
    'GBP-USD': 1.37,
    'JPY-USD': 0.0091,
  };

  const getCurrencyByCode = (code: string): Currency | undefined => {
    return currencies.find(c => c.code === code);
  };

  const getExchangeRate = async (from: string, to: string): Promise<number> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    if (from === to) return 1;
    
    const directRate = mockExchangeRates[`${from}-${to}`];
    if (directRate) return directRate;
    
    const inverseRate = mockExchangeRates[`${to}-${from}`];
    if (inverseRate) return 1 / inverseRate;
    
    // If no direct rate, try via USD
    const fromToUsd = mockExchangeRates[`${from}-USD`] || (from === 'USD' ? 1 : 0);
    const usdToTarget = mockExchangeRates[`USD-${to}`] || (to === 'USD' ? 1 : 0);
    
    if (fromToUsd && usdToTarget) {
      return fromToUsd * usdToTarget;
    }
    
    // Default fallback rate
    return 1.0;
  };

  const convertCurrency = async () => {
    if (!amount || isNaN(parseFloat(amount))) {
      setConvertedAmount('0');
      return;
    }

    setLoading(true);
    try {
      const rate = await getExchangeRate(fromCurrency, toCurrency);
      const converted = parseFloat(amount) * rate;
      setConvertedAmount(converted.toLocaleString('en-US', { 
        minimumFractionDigits: 2, 
        maximumFractionDigits: 8 
      }));
      setExchangeRate(rate);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (error) {
      console.error('Currency conversion error:', error);
      setConvertedAmount('Error');
    } finally {
      setLoading(false);
    }
  };

  const swapCurrencies = () => {
    const temp = fromCurrency;
    setFromCurrency(toCurrency);
    setToCurrency(temp);
  };

  useEffect(() => {
    convertCurrency();
  }, [amount, fromCurrency, toCurrency]);

  const fiatCurrencies = currencies.filter(c => c.type === 'fiat');
  const cryptoCurrencies = currencies.filter(c => c.type === 'crypto');

  const renderCurrencyOption = (currency: Currency) => (
    <option key={currency.code} value={currency.code}>
      {currency.flag} {currency.code} - {currency.name}
    </option>
  );

  const fromCurrencyData = getCurrencyByCode(fromCurrency);
  const toCurrencyData = getCurrencyByCode(toCurrency);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 max-w-md mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Currency Converter
        </h3>
        <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
          <span>🔄</span>
          <span>Live Rates</span>
        </div>
      </div>

      {/* Amount Input */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Amount
        </label>
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                   bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter amount"
          min="0"
          step="any"
        />
      </div>

      {/* From Currency */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          From
        </label>
        <select
          value={fromCurrency}
          onChange={(e) => setFromCurrency(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                   bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <optgroup label="💰 Fiat Currencies">
            {fiatCurrencies.map(renderCurrencyOption)}
          </optgroup>
          <optgroup label="₿ Cryptocurrencies">
            {cryptoCurrencies.map(renderCurrencyOption)}
          </optgroup>
        </select>
      </div>

      {/* Swap Button */}
      <div className="flex justify-center mb-4">
        <button
          onClick={swapCurrencies}
          className="p-2 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400
                   hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors duration-200"
          title="Swap currencies"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                  d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
          </svg>
        </button>
      </div>

      {/* To Currency */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          To
        </label>
        <select
          value={toCurrency}
          onChange={(e) => setToCurrency(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                   bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <optgroup label="💰 Fiat Currencies">
            {fiatCurrencies.map(renderCurrencyOption)}
          </optgroup>
          <optgroup label="₿ Cryptocurrencies">
            {cryptoCurrencies.map(renderCurrencyOption)}
          </optgroup>
        </select>
      </div>

      {/* Result */}
      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {fromCurrencyData?.flag} {amount} {fromCurrency}
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-500">=</div>
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            {loading ? (
              <div className="animate-pulse">Loading...</div>
            ) : (
              <>
                {toCurrencyData?.flag} {convertedAmount} {toCurrency}
              </>
            )}
          </div>
        </div>
        
        {exchangeRate > 0 && !loading && (
          <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-center">
            1 {fromCurrency} = {exchangeRate.toLocaleString('en-US', { 
              minimumFractionDigits: 2, 
              maximumFractionDigits: 8 
            })} {toCurrency}
          </div>
        )}
      </div>

      {/* Last Updated */}
      {lastUpdated && (
        <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
          Last updated: {lastUpdated}
        </div>
      )}

      {/* Quick Convert Buttons */}
      <div className="mt-4 grid grid-cols-3 gap-2">
        {['1', '100', '1000'].map((quickAmount) => (
          <button
            key={quickAmount}
            onClick={() => setAmount(quickAmount)}
            className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-600 text-gray-700 dark:text-gray-300
                     rounded hover:bg-gray-200 dark:hover:bg-gray-500 transition-colors duration-200"
          >
            {quickAmount}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CurrencyConverter;

