import pandas as pd
import numpy as np
import talib
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class TechnicalAnalyzer:
    """技术分析引擎 - 基于TA-Lib专业指标库"""
    
    def __init__(self):
        pass
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """使用TA-Lib计算所有技术指标"""
        df = data.copy()
        
        # 确保数据类型正确
        df['open'] = pd.to_numeric(df['open'], errors='coerce')
        df['high'] = pd.to_numeric(df['high'], errors='coerce')
        df['low'] = pd.to_numeric(df['low'], errors='coerce')
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
        
        # 移动平均线 - 使用TA-Lib
        df['MA5'] = talib.SMA(df['close'], timeperiod=5)
        df['MA10'] = talib.SMA(df['close'], timeperiod=10)
        df['MA20'] = talib.SMA(df['close'], timeperiod=20)
        df['MA60'] = talib.SMA(df['close'], timeperiod=60)
        df['EMA20'] = talib.EMA(df['close'], timeperiod=20)
        df['EMA60'] = talib.EMA(df['close'], timeperiod=60)
        
        # 布林带 - 使用TA-Lib
        bb_upper, bb_middle, bb_lower = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        df['BB_upper'] = bb_upper
        df['BB_middle'] = bb_middle
        df['BB_lower'] = bb_lower
        
        # MACD - 使用TA-Lib
        macd, macd_signal, macd_hist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df['MACD'] = macd
        df['MACD_signal'] = macd_signal
        df['MACD_hist'] = macd_hist
        
        # RSI - 使用TA-Lib
        df['RSI'] = talib.RSI(df['close'], timeperiod=14)
        
        # ADX - 使用TA-Lib
        df['ADX'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
        df['PLUS_DI'] = talib.PLUS_DI(df['high'], df['low'], df['close'], timeperiod=14)
        df['MINUS_DI'] = talib.MINUS_DI(df['high'], df['low'], df['close'], timeperiod=14)
        
        # ATR - 使用TA-Lib
        df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
        
        # 成交量相关指标
        df['Volume_MA5'] = talib.SMA(df['volume'], timeperiod=5)
        df['Volume_Ratio'] = df['volume'] / df['Volume_MA5']
        
        # KDJ指标 - 使用TA-Lib
        df['K'], df['D'] = talib.STOCH(df['high'], df['low'], df['close'], 
                                      fastk_period=9, slowk_period=3, slowk_matype=0, 
                                      slowd_period=3, slowd_matype=0)
        df['J'] = 3 * df['K'] - 2 * df['D']
        
        # 威廉指标 - 使用TA-Lib
        df['WILLR'] = talib.WILLR(df['high'], df['low'], df['close'], timeperiod=14)
        
        # CCI指标 - 使用TA-Lib
        df['CCI'] = talib.CCI(df['high'], df['low'], df['close'], timeperiod=14)
        
        # 随机指标 - 使用TA-Lib
        df['STOCH_K'], df['STOCH_D'] = talib.STOCHF(df['high'], df['low'], df['close'], 
                                                    fastk_period=5, fastd_period=3, fastd_matype=0)
        
        # 动量指标 - 使用TA-Lib
        df['MOM'] = talib.MOM(df['close'], timeperiod=10)
        
        # 价格震荡指标 - 使用TA-Lib
        df['ROC'] = talib.ROC(df['close'], timeperiod=10)
        
        # 成交量价格趋势 - 使用TA-Lib
        df['AD'] = talib.AD(df['high'], df['low'], df['close'], df['volume'])
        df['ADOSC'] = talib.ADOSC(df['high'], df['low'], df['close'], df['volume'], 
                                 fastperiod=3, slowperiod=10)
        
        # 抛物线SAR - 使用TA-Lib
        df['SAR'] = talib.SAR(df['high'], df['low'], acceleration=0.02, maximum=0.2)
        
        # 三重指数移动平均线 - 使用TA-Lib
        df['TRIX'] = talib.TRIX(df['close'], timeperiod=30)
        
        # 终极摆动指标 - 使用TA-Lib
        df['ULTOSC'] = talib.ULTOSC(df['high'], df['low'], df['close'], 
                                   timeperiod1=7, timeperiod2=14, timeperiod3=28)
        
        return df
    
    def identify_band_type(self, data: pd.DataFrame) -> Dict:
        """识别波段类型和位置 - 基于TA-Lib指标"""
        latest = data.iloc[-1]
        recent_5 = data.tail(5)
        recent_15 = data.tail(15)
        
        # 计算价格波动幅度
        price_volatility = data['close'].pct_change().std() * np.sqrt(252)
        
        # 计算波段位置
        band_position = self._analyze_band_position(data)
        
        # 判断波段类型
        band_info = {
            'type': '标准波段',
            'period_range': '5-15天',
            'volatility': price_volatility,
            'trend_strength': latest['ADX'] if not pd.isna(latest['ADX']) else 20,
            'position': band_position['position'],
            'position_description': band_position['description'],
            'guidance': band_position['guidance'],
            'position_percent': band_position['position_percent'],
            'high_20': band_position['high_20'],
            'low_20': band_position['low_20']
        }
        
        # 微型波段：短期高波动 + 高成交量
        if (price_volatility > 0.4 and 
            latest['Volume_Ratio'] > 1.5 and 
            latest['ATR'] > data['ATR'].mean() * 1.2):
            band_info['type'] = '微型波段'
            band_info['period_range'] = '15-30分钟'
        
        # 趋势波段：长期趋势明确 + ADX强
        elif (latest['ADX'] > 30 and 
              self._check_ma_alignment(latest) and
              latest['TRIX'] > 0):
            band_info['type'] = '趋势波段'
            band_info['period_range'] = '15-30天'
        
        # 短线波段：布林带收口 + 低波动
        elif (self._check_bollinger_squeeze(recent_5) and
              price_volatility < 0.2):
            band_info['type'] = '短线波段'
            band_info['period_range'] = '1-3天'
        
        # 震荡波段：RSI在40-60区间 + 低ADX
        elif (40 <= latest['RSI'] <= 60 and
              latest['ADX'] < 20):
            band_info['type'] = '震荡波段'
            band_info['period_range'] = '3-7天'
        
        return band_info
    
    def _analyze_band_position(self, data: pd.DataFrame) -> Dict:
        """分析当前在波段中的位置"""
        latest = data.iloc[-1]
        recent_10 = data.tail(10)
        
        # 计算关键价格水平
        high_20 = data['high'].rolling(20).max().iloc[-1]
        low_20 = data['low'].rolling(20).min().iloc[-1]
        current_price = latest['close']
        
        # 计算在20日高低点之间的位置百分比
        if high_20 != low_20:
            position_percent = (current_price - low_20) / (high_20 - low_20) * 100
        else:
            position_percent = 50
        
        # 判断波段位置
        if position_percent >= 80:
            position = "波段顶部"
            description = "价格接近20日高点，处于波段高位"
            guidance = "注意获利了结，设置止盈位，警惕回调风险"
        elif position_percent >= 60:
            position = "波段中上"
            description = "价格处于波段中上位置，仍有上涨空间"
            guidance = "可继续持有，关注量能配合，设置移动止损"
        elif position_percent >= 40:
            position = "波段中部"
            description = "价格处于波段中部，方向待确认"
            guidance = "观望为主，等待明确信号，可小仓位试探"
        elif position_percent >= 20:
            position = "波段中下"
            description = "价格处于波段中下位置，存在反弹机会"
            guidance = "关注支撑位，可逢低建仓，设置严格止损"
        else:
            position = "波段底部"
            description = "价格接近20日低点，处于波段低位"
            guidance = "关注超跌反弹，可分批建仓，注意风险控制"
        
        # 结合技术指标进一步判断
        rsi = latest['RSI'] if not pd.isna(latest['RSI']) else 50
        macd_signal = latest['MACD'] > latest['MACD_signal']
        
        # 调整指导建议
        if position in ["波段顶部", "波段中上"] and rsi > 70:
            guidance += "，RSI超买，建议减仓"
        elif position in ["波段底部", "波段中下"] and rsi < 30:
            guidance += "，RSI超卖，可考虑抄底"
        elif position == "波段中部" and macd_signal:
            guidance += "，MACD金叉，可适当加仓"
        
        return {
            'position': position,
            'description': description,
            'guidance': guidance,
            'position_percent': position_percent,
            'high_20': high_20,
            'low_20': low_20
        }
    
    def _check_ma_alignment(self, latest_data) -> bool:
        """检查均线多头排列"""
        try:
            return (latest_data['MA5'] > latest_data['MA10'] > 
                   latest_data['MA20'] > latest_data['MA60'])
        except:
            return False
    
    def _check_bollinger_squeeze(self, recent_data) -> bool:
        """检查布林带收口"""
        try:
            bb_width = (recent_data['BB_upper'] - recent_data['BB_lower']) / recent_data['BB_middle']
            return bb_width.iloc[-1] < bb_width.mean() * 0.8
        except:
            return False
    
    def six_dimension_signal_check(self, data: pd.DataFrame, fund_flow: Dict = None) -> Dict:
        """六维信号验证 - 基于TA-Lib指标"""
        latest = data.iloc[-1]
        recent_3 = data.tail(3)
        recent_5 = data.tail(5)
        
        signals = {}
        signal_count = 0
        
        # 1. 趋势方向：均线多头排列 + TRIX确认
        trend_signal = (self._check_ma_alignment(latest) and 
                       latest['TRIX'] > 0 and
                       latest['ADX'] > 25)
        signals['trend_direction'] = {
            'status': trend_signal,
            'strength': 90 if trend_signal else 30,
            'description': '均线多头排列+TRIX确认' if trend_signal else '趋势不明确',
            'details': {
                'ma_alignment': self._check_ma_alignment(latest),
                'trix': latest['TRIX'],
                'adx': latest['ADX']
            }
        }
        if trend_signal:
            signal_count += 1
        
        # 2. 动量强度：RSI + CCI + 威廉指标综合判断
        rsi_value = latest['RSI'] if not pd.isna(latest['RSI']) else 50
        cci_value = latest['CCI'] if not pd.isna(latest['CCI']) else 0
        willr_value = latest['WILLR'] if not pd.isna(latest['WILLR']) else -50
        
        momentum_signal = (45 <= rsi_value <= 75 and
                          -100 <= cci_value <= 100 and
                          -80 <= willr_value <= -20)
        
        signals['momentum_strength'] = {
            'status': momentum_signal,
            'value': rsi_value,
            'description': f'动量指标健康(RSI:{rsi_value:.1f}, CCI:{cci_value:.1f})' if momentum_signal else f'动量指标异常',
            'details': {
                'rsi': rsi_value,
                'cci': cci_value,
                'willr': willr_value
            }
        }
        if momentum_signal:
            signal_count += 1
        
        # 3. 量能配合：成交量 + ADOSC确认
        volume_signal = (latest['Volume_Ratio'] > 1.2 and
                        latest['ADOSC'] > 0)
        signals['volume_cooperation'] = {
            'status': volume_signal,
            'ratio': latest['Volume_Ratio'],
            'description': f'量能配合良好(量比:{latest["Volume_Ratio"]:.1f})' if volume_signal else '量能不足',
            'details': {
                'volume_ratio': latest['Volume_Ratio'],
                'adosc': latest['ADOSC']
            }
        }
        if volume_signal:
            signal_count += 1
        
        # 4. 资金验证：主力资金流入
        fund_signal = False
        if fund_flow and fund_flow['main_net_inflow'] > 0:
            fund_signal = True
            signal_count += 1
        
        fund_data_available = fund_flow is not None and fund_flow.get('main_net_inflow', 0) != 0
        
        signals['fund_verification'] = {
            'status': fund_signal,
            'net_inflow': fund_flow['main_net_inflow'] if fund_flow else 0,
            'description': '主力资金净流入' if fund_signal else ('主力资金流出' if fund_data_available else '资金数据不可用'),
            'data_available': fund_data_available
        }
        
        # 5. 形态确认：突破或回踩 + SAR确认
        pattern_signal = (self._check_pattern_breakthrough(data) and
                         latest['close'] > latest['SAR'])
        signals['pattern_confirmation'] = {
            'status': pattern_signal,
            'description': '形态突破+SAR确认' if pattern_signal else '无明显突破形态',
            'details': {
                'sar_signal': latest['close'] > latest['SAR'],
                'pattern_break': self._check_pattern_breakthrough(data)
            }
        }
        if pattern_signal:
            signal_count += 1
        
        # 6. 市场环境：ADX + 终极摆动指标
        market_signal = (latest['ADX'] > 25 and
                        latest['ULTOSC'] > 30 and latest['ULTOSC'] < 70)
        signals['market_environment'] = {
            'status': market_signal,
            'adx_value': latest['ADX'] if not pd.isna(latest['ADX']) else 20,
            'description': '市场环境良好' if market_signal else '市场环境不佳',
            'details': {
                'adx': latest['ADX'],
                'ultosc': latest['ULTOSC']
            }
        }
        if market_signal:
            signal_count += 1
        
        # 综合评分
        overall_score = (signal_count / 6) * 100
        
        return {
            'signals': signals,
            'signal_count': signal_count,
            'total_signals': 6,  # 六维信号验证
            'overall_score': overall_score,
            'recommendation': self._get_recommendation(signal_count, overall_score)
        }
    
    def _check_pattern_breakthrough(self, data: pd.DataFrame) -> bool:
        """检查突破形态 - 基于TA-Lib指标"""
        if len(data) < 20:
            return False
        
        latest = data.iloc[-1]
        recent_5 = data.tail(5)
        
        # 价格突破布林带上轨
        bb_breakout = latest['close'] > latest['BB_upper']
        
        # MACD金叉
        macd_cross = (latest['MACD'] > latest['MACD_signal'] and
                     data.iloc[-2]['MACD'] <= data.iloc[-2]['MACD_signal'])
        
        # 成交量突破
        volume_breakout = latest['Volume_Ratio'] > 1.5
        
        # 至少满足两个条件
        return sum([bb_breakout, macd_cross, volume_breakout]) >= 2
    
    def analyze_position(self, current_price: float, cost_price: float, position_size: int, 
                        signal_result: Dict, data: pd.DataFrame) -> Dict:
        """持仓分析 - 基于TA-Lib指标"""
        latest = data.iloc[-1]
        
        # 计算盈亏
        profit_loss = (current_price - cost_price) * position_size
        profit_loss_pct = ((current_price - cost_price) / cost_price) * 100
        total_cost = cost_price * position_size
        
        # 基于技术指标的风险评估
        risk_level = '低'
        if latest['RSI'] > 80 or latest['RSI'] < 20:
            risk_level = '高'
        elif latest['RSI'] > 70 or latest['RSI'] < 30:
            risk_level = '中'
        
        # 趋势强度评估
        trend_strength = '弱'
        if latest['ADX'] > 30:
            trend_strength = '强'
        elif latest['ADX'] > 20:
            trend_strength = '中'
        
        # 建议操作
        recommendation = '持有'
        if profit_loss_pct > 10 and latest['RSI'] > 75:
            recommendation = '考虑减仓'
        elif profit_loss_pct < -5 and latest['RSI'] < 25:
            recommendation = '考虑止损'
        elif signal_result['signal_count'] >= 4:
            recommendation = '可加仓'
        
        # 持仓状态
        if profit_loss_pct > 0:
            position_status = '盈利'
        elif profit_loss_pct < 0:
            position_status = '亏损'
        else:
            position_status = '持平'
        
        return {
            'profit_loss': profit_loss,
            'profit_loss_pct': profit_loss_pct,
            'total_cost': total_cost,
            'current_value': current_price * position_size,
            'risk_level': risk_level,
            'trend_strength': trend_strength,
            'recommendation': recommendation,
            'position_status': position_status,  # 添加position_status字段
            'technical_signals': {
                'rsi': latest['RSI'],
                'adx': latest['ADX'],
                'macd_signal': latest['MACD'] > latest['MACD_signal'],
                'bb_position': (current_price - latest['BB_lower']) / (latest['BB_upper'] - latest['BB_lower'])
            }
        }
    
    def generate_trading_decision(self, signal_result: Dict, data: pd.DataFrame, 
                                 position_info: Dict = None) -> Dict:
        """生成交易决策 - 基于TA-Lib指标"""
        latest = data.iloc[-1]
        signal_count = signal_result['signal_count']
        overall_score = signal_result['overall_score']
        
        # 基础决策逻辑
        if signal_count >= 5:
            base_decision = '强烈买入'
            confidence = 90
        elif signal_count >= 4:
            base_decision = '买入'
            confidence = 75
        elif signal_count >= 3:
            base_decision = '谨慎买入'
            confidence = 60
        elif signal_count >= 2:
            base_decision = '观望'
            confidence = 40
        else:
            base_decision = '卖出'
            confidence = 25
        
        # 考虑持仓情况
        if position_info:
            return self._generate_position_based_decision(signal_count, latest['close'], 
                                                        latest['ATR'], position_info, signal_result)
        
        # 计算建议仓位
        position_suggestion = self._calculate_position_suggestion(signal_count, overall_score, latest)
        
        # 风险提示
        risk_warnings = self._generate_risk_warnings(latest)
        
        # 计算目标价位和止损价位
        current_price = latest['close']
        atr = latest['ATR'] if not pd.isna(latest['ATR']) else current_price * 0.02
        
        # 根据信号强度确定目标涨幅
        if signal_count >= 5:
            target_multiplier = 1.15  # 15%目标涨幅
            holding_period = '5-15天'
        elif signal_count >= 4:
            target_multiplier = 1.10  # 10%目标涨幅
            holding_period = '3-7天'
        elif signal_count >= 3:
            target_multiplier = 1.06  # 6%目标涨幅
            holding_period = '1-3天'
        elif signal_count >= 2:
            target_multiplier = 1.03  # 3%目标涨幅
            holding_period = '1-2天'
        else:
            target_multiplier = 1.00  # 无涨幅预期
            holding_period = '观望'
        
        target_price = current_price * target_multiplier
        stop_loss = current_price * 0.95  # 5%止损
        
        return {
            'decision': base_decision,
            'confidence': confidence,
            'signal_count': signal_count,
            'overall_score': overall_score,
            'position_suggestion': position_suggestion,
            'position_ratio': position_suggestion['suggested_position'] / 100,  # 转换为0-1之间的小数
            'target_price': round(target_price, 2),
            'stop_loss': round(stop_loss, 2),
            'holding_period': holding_period,
            'risk_warnings': risk_warnings,
            'technical_reasons': self._get_technical_reasons(signal_result, latest),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _generate_position_based_decision(self, signal_count: int, latest_price: float, 
                                        atr: float, position_info: Dict, signal_result: Dict) -> Dict:
        """基于持仓生成决策"""
        current_price = latest_price
        cost_price = position_info['cost_price']
        position_size = position_info['position_size']
        profit_loss_pct = position_info['profit_loss_pct']
        
        # 持仓决策逻辑
        if signal_count >= 4 and profit_loss_pct < 0:
            decision = '加仓'
            reason = '技术面转好，可逢低加仓'
            confidence = 75
        elif signal_count <= 2 and profit_loss_pct > 5:
            decision = '减仓'
            reason = '技术面转弱，建议获利了结'
            confidence = 70
        elif signal_count <= 1 and profit_loss_pct < -3:
            decision = '止损'
            reason = '技术面恶化，建议止损'
            confidence = 85
        elif signal_count >= 3:
            decision = '持有'
            reason = '技术面良好，继续持有'
            confidence = 80
        else:
            decision = '观望'
            reason = '技术面中性，建议观望'
            confidence = 50
        
        # 根据持仓决策计算目标价位和止损价位
        if decision == '加仓':
            target_price = current_price * 1.12  # 12%目标涨幅
            stop_loss = cost_price * 0.93  # 基于成本价7%止损
            holding_period = '3-10天'
        elif decision == '持有':
            target_price = current_price * 1.08  # 8%目标涨幅
            stop_loss = cost_price * 0.95  # 基于成本价5%止损
            holding_period = '2-7天'
        elif decision == '减仓':
            target_price = current_price * 1.03  # 3%目标涨幅
            stop_loss = cost_price * 0.97  # 基于成本价3%止损
            holding_period = '1-3天'
        elif decision == '止损':
            target_price = current_price  # 无涨幅预期
            stop_loss = current_price * 0.98  # 紧急止损
            holding_period = '立即执行'
        else:  # 观望
            target_price = current_price * 1.05  # 5%目标涨幅
            stop_loss = current_price * 0.95  # 5%止损
            holding_period = '观望等待'
        
        # 计算建议仓位
        position_suggestion = self._calculate_position_suggestion(signal_count, (signal_count / 6) * 100, pd.Series({'ATR': atr, 'close': current_price, 'RSI': 50}))
        
        # 生成风险提示
        risk_warnings = self._generate_risk_warnings(pd.Series({'RSI': 50, 'ADX': 25, 'Volume_Ratio': 1.0, 'close': current_price, 'BB_upper': current_price * 1.05, 'BB_lower': current_price * 0.95}))
        
        # 生成技术面理由，传递真实signal_result
        technical_reasons = self._get_technical_reasons(signal_result, pd.Series({'RSI': 50, 'ADX': 25, 'Volume_Ratio': 1.0, 'close': current_price, 'BB_upper': current_price * 1.05, 'BB_lower': current_price * 0.95}))
        
        return {
            'decision': decision,
            'reason': reason,
            'signal_count': signal_count,
            'overall_score': (signal_count / 6) * 100,  # 添加overall_score字段
            'profit_loss_pct': profit_loss_pct,
            'position_size': position_size,
            'current_price': current_price,
            'cost_price': cost_price,
            'position_ratio': 0.5 if decision in ['加仓', '持有'] else -0.3 if decision == '减仓' else -1.0 if decision == '止损' else 0.0,  # 根据决策设置仓位比例
            'target_price': round(target_price, 2),
            'stop_loss': round(stop_loss, 2),
            'holding_period': holding_period,
            'confidence': confidence,
            'position_suggestion': position_suggestion, # 添加position_suggestion字段
            'risk_warnings': risk_warnings, # 添加risk_warnings字段
            'technical_reasons': technical_reasons, # 添加technical_reasons字段
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _calculate_position_suggestion(self, signal_count: int, overall_score: float, latest: pd.Series) -> Dict:
        """计算建议仓位"""
        # 基础仓位
        base_position = min(signal_count * 20, 100)  # 每个信号20%，最大100%
        
        # 根据ATR调整
        atr_ratio = latest['ATR'] / latest['close']
        if atr_ratio > 0.05:  # 高波动
            base_position *= 0.8
        elif atr_ratio < 0.02:  # 低波动
            base_position *= 1.2
        
        # 根据RSI调整
        if 40 <= latest['RSI'] <= 60:
            base_position *= 1.1  # 中性区间，可适当增加仓位
        elif latest['RSI'] > 70 or latest['RSI'] < 30:
            base_position *= 0.7  # 极值区间，减少仓位
        
        return {
            'suggested_position': round(min(base_position, 100), 1),
            'risk_level': '低' if base_position <= 30 else '中' if base_position <= 60 else '高',
            'reasoning': f'基于{signal_count}个技术信号，建议仓位{round(base_position, 1)}%'
        }
    
    def _generate_risk_warnings(self, latest: pd.Series) -> List[str]:
        """生成风险提示"""
        warnings = []
        
        if latest['RSI'] > 80:
            warnings.append('RSI超买，注意回调风险')
        elif latest['RSI'] < 20:
            warnings.append('RSI超卖，可能存在反弹机会')
        
        if latest['ADX'] < 20:
            warnings.append('趋势强度较弱，建议谨慎操作')
        
        if latest['Volume_Ratio'] < 0.8:
            warnings.append('成交量萎缩，市场活跃度不足')
        
        if latest['close'] > latest['BB_upper']:
            warnings.append('价格突破布林带上轨，注意回调')
        elif latest['close'] < latest['BB_lower']:
            warnings.append('价格跌破布林带下轨，可能存在超跌反弹')
        
        return warnings
    
    def _get_technical_reasons(self, signal_result: Dict, latest: pd.Series) -> List[str]:
        """获取技术面理由"""
        reasons = []
        signals = signal_result['signals']
        
        if signals['trend_direction']['status']:
            reasons.append('趋势方向明确，均线多头排列')
        
        if signals['momentum_strength']['status']:
            reasons.append('动量指标健康，RSI在理想区间')
        
        if signals['volume_cooperation']['status']:
            reasons.append('量能配合良好，成交量放大')
        
        if signals['pattern_confirmation']['status']:
            reasons.append('形态突破确认，SAR指标支持')
        
        if signals['market_environment']['status']:
            reasons.append('市场环境良好，ADX显示趋势明确')
        
        return reasons
    
    def _get_recommendation(self, signal_count: int, overall_score: float) -> str:
        """获取综合建议"""
        if signal_count >= 5 and overall_score >= 80:
            return '强烈推荐买入'
        elif signal_count >= 4 and overall_score >= 65:
            return '推荐买入'
        elif signal_count >= 3 and overall_score >= 50:
            return '谨慎买入'
        elif signal_count >= 2:
            return '观望为主'
        else:
            return '建议卖出或观望'
    
    def calculate_position_management(self, decision: Dict, latest_price: float) -> Dict:
        """仓位管理建议"""
        suggested_position = decision.get('position_suggestion', {}).get('suggested_position', 0)
        signal_count = decision.get('signal_count', 0)
        
        # 根据信号强度调整仓位分配策略
        if signal_count >= 5:
            # 强烈信号：激进配置
            bottom_position = 0.6    # 60%底仓
            breakout_add = 0.25      # 25%突破加仓
            pullback_add = 0.10      # 10%回调补仓
            flexible_trade = 0.05    # 5%机动T+0
        elif signal_count >= 4:
            # 较强信号：标准配置
            bottom_position = 0.5    # 50%底仓
            breakout_add = 0.25      # 25%突破加仓
            pullback_add = 0.15      # 15%回调补仓
            flexible_trade = 0.10    # 10%机动T+0
        elif signal_count >= 3:
            # 中等信号：保守配置
            bottom_position = 0.4    # 40%底仓
            breakout_add = 0.30      # 30%突破加仓
            pullback_add = 0.20      # 20%回调补仓
            flexible_trade = 0.10    # 10%机动T+0
        elif signal_count >= 2:
            # 弱信号：谨慎配置
            bottom_position = 0.3    # 30%底仓
            breakout_add = 0.35      # 35%突破加仓
            pullback_add = 0.25      # 25%回调补仓
            flexible_trade = 0.10    # 10%机动T+0
        else:
            # 无信号：观望配置
            bottom_position = 0.0    # 0%底仓
            breakout_add = 0.0       # 0%突破加仓
            pullback_add = 0.0       # 0%回调补仓
            flexible_trade = 0.0     # 0%机动T+0
        
        return {
            'suggested_position': suggested_position,
            'position_strategy': '分批建仓' if suggested_position > 50 else '一次性建仓',
            'bottom_position': bottom_position,
            'breakout_add': breakout_add,
            'pullback_add': pullback_add,
            'flexible_trade': flexible_trade,
            'stop_loss': latest_price * 0.95,  # 5%止损
            'take_profit': latest_price * 1.15,  # 15%止盈
            'risk_management': '建议设置止损止盈，控制单笔交易风险'
        }
    
    def calculate_stop_profit_loss(self, latest_price: float, atr: float) -> Dict:
        """计算止盈止损 - 基于ATR"""
        if pd.isna(atr) or atr == 0:
            atr = latest_price * 0.02  # 默认2%
        
        stop_loss = latest_price - (atr * 2)  # 2倍ATR止损
        take_profit = latest_price + (atr * 3)  # 3倍ATR止盈
        
        # 阶梯止盈
        step_profit = {
            '15%': round(latest_price * 1.15, 2),
            '25%': round(latest_price * 1.25, 2),
            '40%': round(latest_price * 1.40, 2)
        }
        
        # 移动止损（基于7%回撤）
        trailing_stop = round(latest_price * 0.93, 2)
        
        # 紧急止损（基于2倍ATR）
        emergency_stop = round(latest_price - (atr * 2), 2)
        
        return {
            'stop_loss': round(stop_loss, 2),
            'take_profit': round(take_profit, 2),
            'stop_loss_pct': round(((stop_loss - latest_price) / latest_price) * 100, 2),
            'take_profit_pct': round(((take_profit - latest_price) / latest_price) * 100, 2),
            'step_profit': step_profit,
            'trailing_stop': trailing_stop,
            'emergency_stop': emergency_stop,
            'time_stop': 5,  # 5日时间止损
            'atr': round(atr, 2),
            'method': '基于ATR动态计算'
        } 