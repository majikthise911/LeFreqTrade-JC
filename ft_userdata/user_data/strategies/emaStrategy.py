# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# This class is a sample. Feel free to customize it.
class emaStrategy(IStrategy):
    """
    This is a sample strategy to inspire you.
    More information in https://www.freqtrade.io/en/latest/strategy-customization/

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the methods: populate_indicators, populate_entry_trend, populate_exit_trend
    You should keep:
    - timeframe, minimal_roi, stoploss, trailing_*
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 0.152,
        "105": 0.117,
        "255": 0.028,
        "565": 0
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.10

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Optimal timeframe for the strategy.
    timeframe = '1m'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Hyperoptable parameters
    buy_rsi = IntParameter(low=1, high=50, default=30, space='buy', optimize=True, load=True)
    sell_rsi = IntParameter(low=50, high=100, default=70, space='sell', optimize=True, load=True)
    short_rsi = IntParameter(low=51, high=100, default=70, space='sell', optimize=True, load=True)
    exit_short_rsi = IntParameter(low=1, high=50, default=30, space='buy', optimize=True, load=True)

   # buy_ema = IntParameter(low=1, high=50, default=30, space='buy', optimize=True, load=True)
   # sell_ema = IntParameter(low=50, high=100, default=70, space='sell', optimize=True, load=True)
   # short_ema = IntParameter(low=51, high=100, default=70, space='sell', optimize=True, load=True)
   # exit_short_ema = IntParameter(low=1, high=50, default=30, space='buy', optimize=True, load=True)
    
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 5

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }

    plot_config = {
        'main_plot': {
            'tema': {},
            'sar': {'color': 'white'},
        },
        'subplots': {
            "MACD": {
                'macd': {'color': 'blue'},
                'macdsignal': {'color': 'orange'},
            },
            "RSI": {
                'rsi': {'color': 'red'},
            }
        }
    }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # Momentum Indicators
        # ------------------------------------

        # ADX
        dataframe['adx'] = ta.ADX(dataframe)


        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)


        # Stochastic Fast
        stoch_fast = ta.STOCHF(dataframe)
        dataframe['fastd'] = stoch_fast['fastd']
        dataframe['fastk'] = stoch_fast['fastk']


        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        # MFI
        dataframe['mfi'] = ta.MFI(dataframe)

        # # ROC
        # dataframe['roc'] = ta.ROC(dataframe)

        # Overlap Studies
        # ------------------------------------

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe["bb_percent"] = (
            (dataframe["close"] - dataframe["bb_lowerband"]) /
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"])
        )
        dataframe["bb_width"] = (
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"]) / dataframe["bb_middleband"]
        )


        # # EMA - Exponential Moving Average
        # dataframe['ema3'] = ta.EMA(dataframe, timeperiod=3)
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        # dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        # dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)

        # # SMA - Simple Moving Average
        # dataframe['sma3'] = ta.SMA(dataframe, timeperiod=3)
        dataframe['sma5'] = ta.SMA(dataframe, timeperiod=5)
        # dataframe['sma10'] = ta.SMA(dataframe, timeperiod=10)
        dataframe['sma21'] = ta.SMA(dataframe, timeperiod=21)
        # dataframe['sma50'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['sma100'] = ta.SMA(dataframe, timeperiod=100)

        # Parabolic SAR
        dataframe['sar'] = ta.SAR(dataframe)

        # TEMA - Triple Exponential Moving Average
        dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)

        # Cycle Indicator
        # ------------------------------------
        # Hilbert Transform Indicator - SineWave
        hilbert = ta.HT_SINE(dataframe)
        dataframe['htsine'] = hilbert['sine']
        dataframe['htleadsine'] = hilbert['leadsine']

        # # Chart type
        # # ------------------------------------
        # # Heikin Ashi Strategy
        # heikinashi = qtpylib.heikinashi(dataframe)
        # dataframe['ha_open'] = heikinashi['open']
        # dataframe['ha_close'] = heikinashi['close']
        # dataframe['ha_high'] = heikinashi['high']
        # dataframe['ha_low'] = heikinashi['low']

        # Retrieve best bid and best ask from the orderbook
        # ------------------------------------


        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        dataframe.loc[
         (
             (dataframe['ema5'] > dataframe['ema21']) & 
             (dataframe['ema5'] > dataframe['sma21']) & 
             (dataframe['ema5'].shift(1) <= dataframe['ema21'])
             ),
             'buy'] = 1


        # dataframe.loc[
        #     (
        #         # Signal: RSI crosses above 30
        #         (qtpylib.crossed_above(dataframe['rsi'], self.buy_rsi.value)) &
        #         (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard: tema below BB middle
        #         (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard: tema is raising
        #         (dataframe['volume'] > 0)  # Make sure Volume is not 0
        #     ),
        #     'enter_long'] = 1

        # dataframe.loc[
        #     (
        #         # Signal: RSI crosses above 70
        #         (qtpylib.crossed_above(dataframe['rsi'], self.short_rsi.value)) &
        #         (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard: tema above BB middle
        #         (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard: tema is falling
        #         (dataframe['volume'] > 0)  # Make sure Volume is not 0
        #     ),
        #     'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with exit columns populated
        """
        # dataframe.loc[
        #     (
        #         # Signal: RSI crosses above 70
        #         (qtpylib.crossed_above(dataframe['rsi'], self.sell_rsi.value)) &
        #         (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard: tema above BB middle
        #         (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard: tema is falling
        #         (dataframe['volume'] > 0)  # Make sure Volume is not 0
        #     ),

        #     'exit_long'] = 1

        dataframe.loc[
         (
             (dataframe['ema5'] < dataframe['ema21']) & 
             (dataframe['ema5'] < dataframe['sma21']) & 
             (dataframe['ema5'].shift(1) > dataframe['ema21'])
             ),
             'sell'] = 1


        # dataframe.loc[
        #     (
        #         # Signal: RSI crosses above 30
        #         (qtpylib.crossed_above(dataframe['rsi'], self.exit_short_rsi.value)) &
        #         # Guard: tema below BB middle
        #         (dataframe['tema'] <= dataframe['bb_middleband']) &
        #         (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard: tema is raising
        #         (dataframe['volume'] > 0)  # Make sure Volume is not 0
        #     ),
        #     'exit_short'] = 1

        return dataframe
