import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict

class StockVisualizer:
    """股票可视化模块"""
    
    def __init__(self):
        self.colors = {
            'bullish': '#00C853',
            'bearish': '#FF1744',
            'neutral': '#757575',
            'volume': '#1976D2',
            'ma': ['#FF9800', '#2196F3', '#9C27B0', '#4CAF50'],
            'background': '#FAFAFA'
        }
    
    def create_stock_chart(self, data: pd.DataFrame, stock_info: Dict, 
                          signals: Dict = None, band_info: Dict = None) -> go.Figure:
        """创建完整的股票分析图表"""
        
        # 创建子图
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,
            subplot_titles=['价格走势', 'MACD', 'RSI', '成交量'],
            row_width=[0.5, 0.15, 0.15, 0.2]
        )
        
        # 1. K线图（红色上涨，绿色下跌）
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name='K线',
                increasing_line_color='red',  # 上涨用红色
                decreasing_line_color='green'  # 下跌用绿色
            ), row=1, col=1
        )
        
        # 添加移动平均线
        ma_colors = self.colors['ma']
        ma_periods = [5, 10, 20, 60]
        ma_names = ['MA5', 'MA10', 'MA20', 'MA60']
        
        for i, (period, name) in enumerate(zip(ma_periods, ma_names)):
            if name in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data[name],
                        mode='lines',
                        name=name,
                        line=dict(color=ma_colors[i % len(ma_colors)], width=1),
                        opacity=0.8
                    ), row=1, col=1
                )
        
        # 添加布林带
        if all(col in data.columns for col in ['BB_upper', 'BB_middle', 'BB_lower']):
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['BB_upper'],
                    mode='lines',
                    name='布林上轨',
                    line=dict(color='rgba(128,128,128,0.3)', width=1),
                    showlegend=False
                ), row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['BB_lower'],
                    mode='lines',
                    name='布林下轨',
                    line=dict(color='rgba(128,128,128,0.3)', width=1),
                    fill='tonexty',
                    fillcolor='rgba(128,128,128,0.1)',
                    showlegend=False
                ), row=1, col=1
            )
        
        # 2. MACD指标
        if all(col in data.columns for col in ['MACD', 'MACD_signal', 'MACD_hist']):
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MACD'],
                    mode='lines',
                    name='MACD',
                    line=dict(color=self.colors['bullish'], width=2)
                ), row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MACD_signal'],
                    mode='lines',
                    name='Signal',
                    line=dict(color=self.colors['bearish'], width=2)
                ), row=2, col=1
            )
            
            # MACD柱状图（红色上涨，绿色下跌）
            colors = ['green' if val < 0 else 'red' for val in data['MACD_hist']]
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data['MACD_hist'],
                    name='MACD Hist',
                    marker_color=colors,
                    opacity=0.6
                ), row=2, col=1
            )
        
        # 3. RSI指标
        if 'RSI' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['RSI'],
                    mode='lines',
                    name='RSI',
                    line=dict(color=self.colors['volume'], width=2)
                ), row=3, col=1
            )
            
            # 添加RSI的超买超卖线（红色超买，绿色超卖）
            fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.7, row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.7, row=3, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color="gray", opacity=0.5, row=3, col=1)
        
        # 4. 成交量（红色上涨，绿色下跌）
        volume_colors = []
        for i in range(len(data)):
            if i > 0:
                if data['close'].iloc[i] > data['close'].iloc[i-1]:
                    volume_colors.append('red')  # 上涨用红色
                else:
                    volume_colors.append('green')  # 下跌用绿色
            else:
                volume_colors.append(self.colors['neutral'])
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['volume'],
                name='成交量',
                marker_color=volume_colors,
                opacity=0.7
            ), row=4, col=1
        )
        
        # 添加成交量移动平均线
        if 'Volume_MA5' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['Volume_MA5'],
                    mode='lines',
                    name='成交量MA5',
                    line=dict(color='orange', width=2)
                ), row=4, col=1
            )
        
        # 更新布局
        fig.update_layout(
            title=f'{stock_info.get("name", "未知股票")} - 波段分析图表',
            height=800,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            template='plotly_white'
        )
        
        # 更新各子图的y轴标题
        fig.update_yaxes(title_text="价格(元)", row=1, col=1)
        fig.update_yaxes(title_text="MACD", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1)
        fig.update_yaxes(title_text="成交量", row=4, col=1)
        
        return fig
    
    def generate_signal_card(self, stock_info: Dict, realtime_data: Dict,
                           signal_result: Dict, decision: Dict, 
                           band_info: Dict, data: pd.DataFrame) -> str:
        """生成操作建议卡片"""
        
        # 获取当前数据
        latest_price = data.iloc[-1]['close']
        support_level = data['close'].quantile(0.2)
        resistance_level = data['close'].quantile(0.8)
        
        # 信号验证状态
        signals = signal_result['signals']
        signal_icons = []
        
        for key, signal in signals.items():
            icon = "✅" if signal['status'] else "❌"
            if key == 'trend_direction':
                signal_icons.append(f"{icon} 趋势方向：{signal['description']}")
            elif key == 'momentum_strength':
                signal_icons.append(f"{icon} 动量强度：{signal['description']}")
            elif key == 'volume_cooperation':
                signal_icons.append(f"{icon} 量能配合：{signal['description']}")
            elif key == 'fund_verification':
                signal_icons.append(f"{icon} 资金验证：{signal['description']}")
            elif key == 'pattern_confirmation':
                signal_icons.append(f"{icon} 形态确认：{signal['description']}")
            elif key == 'market_environment':
                signal_icons.append(f"{icon} 市场环境：{signal['description']}")
        
        # 操作建议颜色
        action_color = "🟢" if "买入" in decision['action'] else "⚠️" if "试单" in decision['action'] else "🔴"
        
        # 生成卡片
        card = f"""
**【波段操作信号卡】**
**股票：{stock_info.get('name', '未知')}**  **更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**▶ 波段状态：** {band_info['type']}（预期周期{band_info['period_range']}）

**▶ 关键位置：**
- 支撑位：￥{support_level:.2f}
- 压力位：￥{resistance_level:.2f}
- 当前价：￥{latest_price:.2f}

**▶ 信号验证：** ({signal_result['signal_count']}/{signal_result['total_signals']})
"""
        
        for signal_desc in signal_icons:
            card += f"  {signal_desc}\n"
        
        card += f"""
**▶ 操作建议：**
  {action_color} **{decision['action']}** (建议仓位: {decision['position_ratio']*100:.0f}%)
  🎯 目标价位：￥{decision['target_price']:.2f} ({((decision['target_price']/latest_price-1)*100):+.1f}%)
  ⛔ 止损价位：￥{decision['stop_loss']:.2f} ({((decision['stop_loss']/latest_price-1)*100):+.1f}%)
  ⏰ 建议持有：{decision['holding_period']}

**▶ 风险提示：** 
本分析基于技术指标，仅供参考，投资有风险，决策需谨慎。
"""
        
        return card
    
    def create_risk_dashboard(self, position_mgmt: Dict, stop_strategy: Dict) -> str:
        """创建风险管理看板"""
        
        dashboard = f"""
**【风险管理看板】**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**▶ 仓位分配策略：**
- 🏗️ 底仓配置：{position_mgmt['bottom_position']*100:.1f}%
- 📈 突破加仓：{position_mgmt['breakout_add']*100:.1f}%
- 📉 回调补仓：{position_mgmt['pullback_add']*100:.1f}%
- 🔄 机动T+0：{position_mgmt['flexible_trade']*100:.1f}%

**▶ 止盈止损设置：**
- 🎯 阶梯止盈：
  - 15%收益：￥{stop_strategy['step_profit']['15%']:.2f}
  - 25%收益：￥{stop_strategy['step_profit']['25%']:.2f}
  - 40%收益：￥{stop_strategy['step_profit']['40%']:.2f}
- 🛡️ 移动止损：￥{stop_strategy['trailing_stop']:.2f} (7%回撤)
- ⏰ 时间止损：{stop_strategy['time_stop']}日
- 🚨 紧急止损：￥{stop_strategy['emergency_stop']:.2f}
"""
        
        return dashboard 