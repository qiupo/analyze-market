import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class TechnicalAnalyzer:
    """技术分析引擎"""
    
    def __init__(self):
        pass
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算所有技术指标"""
        df = data.copy()
        
        # 移动平均线
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA10'] = df['close'].rolling(window=10).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA60'] = df['close'].rolling(window=60).mean()
        df['EMA20'] = df['close'].ewm(span=20).mean()
        df['EMA60'] = df['close'].ewm(span=60).mean()
        
        # 布林带
        bb_middle = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['BB_upper'] = bb_middle + (bb_std * 2)
        df['BB_middle'] = bb_middle
        df['BB_lower'] = bb_middle - (bb_std * 2)
        
        # MACD
        exp1 = df['close'].ewm(span=12).mean()
        exp2 = df['close'].ewm(span=26).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_hist'] = df['MACD'] - df['MACD_signal']
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # ADX (简化版本)
        high_low = df['high'] - df['low']
        high_close_prev = abs(df['high'] - df['close'].shift(1))
        low_close_prev = abs(df['low'] - df['close'].shift(1))
        tr = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
        atr = tr.rolling(window=14).mean()
        
        plus_dm = df['high'].diff()
        minus_dm = df['low'].diff()
        plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0)
        minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)
        
        plus_di = 100 * (plus_dm.rolling(window=14).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=14).mean() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        df['ADX'] = dx.rolling(window=14).mean()
        
        # ATR (平均真实波幅)
        df['ATR'] = atr
        
        # 成交量相关
        df['Volume_MA5'] = df['volume'].rolling(window=5).mean()
        df['Volume_Ratio'] = df['volume'] / df['Volume_MA5']
        
        # KDJ指标 (简化版本)
        low_min = df['low'].rolling(window=9).min()
        high_max = df['high'].rolling(window=9).max()
        rsv = (df['close'] - low_min) / (high_max - low_min) * 100
        df['K'] = rsv.ewm(com=2).mean()
        df['D'] = df['K'].ewm(com=2).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']
        
        return df
    
    def identify_band_type(self, data: pd.DataFrame) -> Dict:
        """识别波段类型"""
        latest = data.iloc[-1]
        recent_5 = data.tail(5)
        recent_15 = data.tail(15)
        
        # 计算价格波动幅度
        price_volatility = data['close'].pct_change().std() * np.sqrt(252)
        
        # 判断波段类型
        band_info = {
            'type': '标准波段',
            'period_range': '5-15天',
            'volatility': price_volatility,
            'trend_strength': latest['ADX'] if not pd.isna(latest['ADX']) else 20
        }
        
        # 微型波段：短期高波动
        if price_volatility > 0.4 and latest['Volume_Ratio'] > 1.5:
            band_info['type'] = '微型波段'
            band_info['period_range'] = '15-30分钟'
        
        # 趋势波段：长期趋势明确
        elif latest['ADX'] > 30 and self._check_ma_alignment(latest):
            band_info['type'] = '趋势波段'
            band_info['period_range'] = '15-30天'
        
        # 短线波段：布林带收口
        elif self._check_bollinger_squeeze(recent_5):
            band_info['type'] = '短线波段'
            band_info['period_range'] = '1-3天'
        
        return band_info
    
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
        """六维信号验证"""
        latest = data.iloc[-1]
        recent_3 = data.tail(3)
        recent_5 = data.tail(5)
        
        signals = {}
        signal_count = 0
        
        # 1. 趋势方向：20/60日均线多头排列
        trend_signal = self._check_ma_alignment(latest)
        signals['trend_direction'] = {
            'status': trend_signal,
            'strength': 85 if trend_signal else 30,
            'description': '20/60日均线多头排列' if trend_signal else '均线排列不佳'
        }
        if trend_signal:
            signal_count += 1
        
        # 2. 动量强度：RSI(14)在45-75区间
        rsi_value = latest['RSI'] if not pd.isna(latest['RSI']) else 50
        momentum_signal = 45 <= rsi_value <= 75
        signals['momentum_strength'] = {
            'status': momentum_signal,
            'value': rsi_value,
            'description': f'RSI({rsi_value:.1f})在理想区间' if momentum_signal else f'RSI({rsi_value:.1f})过热或过冷'
        }
        if momentum_signal:
            signal_count += 1
        
        # 3. 量能配合：成交量>5日均量120%
        volume_signal = latest['Volume_Ratio'] > 1.2
        signals['volume_cooperation'] = {
            'status': volume_signal,
            'ratio': latest['Volume_Ratio'],
            'description': f'成交量放大{latest["Volume_Ratio"]:.1f}倍' if volume_signal else '成交量不足'
        }
        if volume_signal:
            signal_count += 1
        
        # 4. 资金验证：主力资金流入（如果数据不可用则跳过）
        fund_signal = False
        if fund_flow and fund_flow['main_net_inflow'] > 0:
            fund_signal = True
            signal_count += 1
        
        # 检查资金流向数据是否可用
        fund_data_available = fund_flow is not None and fund_flow.get('main_net_inflow', 0) != 0
        
        signals['fund_verification'] = {
            'status': fund_signal,
            'net_inflow': fund_flow['main_net_inflow'] if fund_flow else 0,
            'description': '主力资金净流入' if fund_signal else ('主力资金流出' if fund_data_available else '资金数据不可用'),
            'data_available': fund_data_available
        }
        
        # 5. 形态确认：突破或回踩
        pattern_signal = self._check_pattern_breakthrough(data)
        signals['pattern_confirmation'] = {
            'status': pattern_signal,
            'description': '形态突破确认' if pattern_signal else '无明显突破形态'
        }
        if pattern_signal:
            signal_count += 1
        
        # 6. 市场环境：简化版本（基于ADX）
        market_signal = latest['ADX'] > 25 if not pd.isna(latest['ADX']) else False
        signals['market_environment'] = {
            'status': market_signal,
            'adx_value': latest['ADX'] if not pd.isna(latest['ADX']) else 20,
            'description': '市场趋势明确' if market_signal else '市场震荡整理'
        }
        if market_signal:
            signal_count += 1
        
        # 计算实际可用的信号总数
        total_signals = 6
        if not fund_data_available:
            total_signals = 5  # 资金验证信号不可用时，总数为5
        
        return {
            'signals': signals,
            'signal_count': signal_count,
            'total_signals': total_signals
        }
    
    def _check_pattern_breakthrough(self, data: pd.DataFrame) -> bool:
        """检查形态突破"""
        recent_20 = data.tail(20)
        latest_price = data.iloc[-1]['close']
        
        # 简化的突破判断：价格突破20日内的重要阻力位
        resistance_level = recent_20['high'].quantile(0.8)
        support_level = recent_20['low'].quantile(0.2)
        
        # 如果当前价格突破阻力位或在支撑位上方
        return latest_price > resistance_level or latest_price > support_level * 1.02
    
    def analyze_position(self, current_price: float, cost_price: float, position_size: int, 
                        signal_result: Dict, data: pd.DataFrame) -> Dict:
        """分析当前持仓情况"""
        if position_size <= 0 or cost_price <= 0:
            return None
        
        # 计算盈亏
        total_cost = cost_price * position_size
        current_value = current_price * position_size
        profit_loss = current_value - total_cost
        profit_loss_pct = (profit_loss / total_cost) * 100
        
        # 计算技术位置
        atr = data.iloc[-1]['ATR'] if not pd.isna(data.iloc[-1]['ATR']) else current_price * 0.02
        
        # 持仓状态分析
        if profit_loss_pct > 15:
            position_status = "大幅盈利"
            risk_level = "低"
        elif profit_loss_pct > 5:
            position_status = "适度盈利"
            risk_level = "中低"
        elif profit_loss_pct > -5:
            position_status = "盈亏平衡"
            risk_level = "中等"
        elif profit_loss_pct > -15:
            position_status = "浮亏状态"
            risk_level = "中高"
        else:
            position_status = "深度套牢"
            risk_level = "高"
        
        return {
            'total_cost': total_cost,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_pct': profit_loss_pct,
            'position_status': position_status,
            'risk_level': risk_level,
            'stop_loss_price': cost_price * 0.92,  # 8%止损
            'take_profit_price': cost_price * 1.15  # 15%止盈
        }
    
    def generate_trading_decision(self, signal_result: Dict, data: pd.DataFrame, 
                                 position_info: Dict = None) -> Dict:
        """生成交易决策"""
        signal_count = signal_result['signal_count']
        latest_price = data.iloc[-1]['close']
        atr = data.iloc[-1]['ATR'] if not pd.isna(data.iloc[-1]['ATR']) else latest_price * 0.02
        
        # 如果有持仓信息，生成个性化建议
        if position_info is not None:
            return self._generate_position_based_decision(signal_count, latest_price, atr, position_info)
        
        # 无持仓情况：标准买卖点决策矩阵
        if signal_count >= 5:
            decision = {
                'action': '重仓建仓',
                'position_ratio': 0.75,
                'holding_period': '5-15天',
                'confidence': '高',
                'target_price': latest_price * 1.15,
                'stop_loss': latest_price - 2 * atr,
                'suggestion_type': 'new_position'
            }
        elif signal_count >= 3:
            decision = {
                'action': '标准建仓',
                'position_ratio': 0.45,
                'holding_period': '3-7天',
                'confidence': '中',
                'target_price': latest_price * 1.08,
                'stop_loss': latest_price - 1.5 * atr,
                'suggestion_type': 'new_position'
            }
        elif signal_count >= 2:
            decision = {
                'action': '轻仓试单',
                'position_ratio': 0.15,
                'holding_period': '1-3天',
                'confidence': '低',
                'target_price': latest_price * 1.05,
                'stop_loss': latest_price - atr,
                'suggestion_type': 'new_position'
            }
        else:
            decision = {
                'action': '暂不建仓',
                'position_ratio': 0.0,
                'holding_period': '-',
                'confidence': '观望',
                'target_price': latest_price,
                'stop_loss': latest_price,
                'suggestion_type': 'wait'
            }
        
        return decision
    
    def _generate_position_based_decision(self, signal_count: int, latest_price: float, 
                                        atr: float, position_info: Dict) -> Dict:
        """基于持仓情况生成个性化交易决策"""
        profit_loss_pct = position_info['profit_loss_pct']
        cost_price = position_info['total_cost'] / position_info.get('position_size', 1)
        
        # 根据盈亏情况和信号强度决定操作
        if profit_loss_pct > 15:  # 大幅盈利
            if signal_count >= 4:
                action = '持有并加仓'
                suggestion_type = 'hold_and_add'
            elif signal_count >= 2:
                action = '继续持有'
                suggestion_type = 'hold'
            else:
                action = '考虑减仓'
                suggestion_type = 'reduce'
        elif profit_loss_pct > 5:  # 适度盈利
            if signal_count >= 5:
                action = '持有并加仓'
                suggestion_type = 'hold_and_add'
            elif signal_count >= 3:
                action = '继续持有'
                suggestion_type = 'hold'
            else:
                action = '保持观望'
                suggestion_type = 'hold'
        elif profit_loss_pct > -5:  # 盈亏平衡
            if signal_count >= 5:
                action = '逢低加仓'
                suggestion_type = 'add_on_dip'
            elif signal_count >= 3:
                action = '继续持有'
                suggestion_type = 'hold'
            else:
                action = '考虑止盈'
                suggestion_type = 'take_profit'
        elif profit_loss_pct > -15:  # 浮亏状态
            if signal_count >= 5:
                action = '补仓摊薄'
                suggestion_type = 'average_down'
            elif signal_count >= 3:
                action = '继续持有'
                suggestion_type = 'hold'
            else:
                action = '考虑止损'
                suggestion_type = 'stop_loss'
        else:  # 深度套牢
            if signal_count >= 5:
                action = '分批补仓'
                suggestion_type = 'dollar_cost_average'
            elif signal_count >= 2:
                action = '耐心持有'
                suggestion_type = 'patient_hold'
            else:
                action = '坚决止损'
                suggestion_type = 'cut_loss'
        
        # 计算建议仓位比例
        if suggestion_type in ['hold_and_add', 'add_on_dip', 'average_down']:
            position_ratio = min(0.3, 0.1 * signal_count)  # 最多加仓30%
        elif suggestion_type in ['reduce', 'take_profit']:
            position_ratio = -0.3  # 减仓30%
        elif suggestion_type in ['stop_loss', 'cut_loss']:
            position_ratio = -1.0  # 全部清仓
        else:
            position_ratio = 0.0  # 维持现状
        
        return {
            'action': action,
            'position_ratio': position_ratio,
            'holding_period': '根据技术面调整',
            'confidence': '高' if signal_count >= 4 else '中' if signal_count >= 2 else '低',
            'target_price': latest_price * 1.1 if position_ratio > 0 else latest_price,
            'stop_loss': cost_price * 0.92,  # 基于成本价的止损
            'suggestion_type': suggestion_type,
            'current_profit_loss': profit_loss_pct
        }
    
    def calculate_position_management(self, decision: Dict, latest_price: float) -> Dict:
        """计算仓位管理策略"""
        if decision['action'] == '保持观望':
            return {
                'bottom_position': 0,
                'breakout_add': 0,
                'pullback_add': 0,
                'flexible_trade': 0
            }
        
        total_ratio = decision['position_ratio']
        
        return {
            'bottom_position': total_ratio * 0.5,  # 50%底仓
            'breakout_add': total_ratio * 0.25,    # 25%突破加仓
            'pullback_add': total_ratio * 0.15,    # 15%回调补仓
            'flexible_trade': total_ratio * 0.1    # 10%机动T+0
        }
    
    def calculate_stop_profit_loss(self, latest_price: float, atr: float) -> Dict:
        """计算止盈止损策略"""
        return {
            'step_profit': {
                '15%': latest_price * 1.15,  # 第一阶梯止盈
                '25%': latest_price * 1.25,  # 第二阶梯止盈
                '40%': latest_price * 1.40   # 第三阶梯止盈
            },
            'trailing_stop': latest_price * 0.93,  # 7%移动止损
            'time_stop': 5,  # 5日时间止损
            'emergency_stop': latest_price - 2 * atr  # 紧急止损
        } 