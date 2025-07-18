import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 导入自定义模块
from src.core.data_fetcher import StockDataFetcher
from src.core.technical_analysis import TechnicalAnalyzer
from src.core.visualization import StockVisualizer

# 配置页面
st.set_page_config(
    page_title="智策波段交易助手",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .signal-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.8rem;
        border: 2px solid #4CAF50;
        margin: 1rem 0;
        font-family: 'Arial', sans-serif;
        color: #333333;
        font-size: 14px;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.8rem;
        border: 2px solid #FF9800;
        margin: 1rem 0;
        font-family: 'Arial', sans-serif;
        color: #333333;
        font-size: 14px;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # 缓存5分钟，只缓存基础数据
def load_basic_stock_data(symbol, period=100):
    """加载股票基础数据（带缓存）"""
    fetcher = StockDataFetcher()
    data = fetcher.get_stock_data(symbol, period)
    stock_info = fetcher.get_stock_info(symbol)
    fund_flow = fetcher.get_fund_flow(symbol)
    
    return data, stock_info, fund_flow

@st.cache_data(ttl=60)  # 分析结果缓存1分钟，基于股票和持仓信息
def analyze_stock_cached(symbol, period, has_position, current_position, cost_price, data_hash):
    """带缓存的股票分析（基于持仓信息）"""
    # 重新获取基础数据（使用缓存）
    data, stock_info, fund_flow = load_basic_stock_data(symbol, period)
    
    if data is None or data.empty:
        return None
    
    return analyze_stock_core(data, fund_flow, has_position, current_position, cost_price)

def analyze_stock_core(data, fund_flow, has_position=False, current_position=0, cost_price=0):
    """核心分析逻辑（不缓存）"""
    analyzer = TechnicalAnalyzer()
    
    # 计算技术指标
    data_with_indicators = analyzer.calculate_indicators(data)
    
    # 识别波段类型
    band_info = analyzer.identify_band_type(data_with_indicators)
    
    # 六维信号验证
    signal_result = analyzer.six_dimension_signal_check(data_with_indicators, fund_flow)
    
    # 获取当前价格
    latest_price = data_with_indicators.iloc[-1]['close']
    
    # 持仓分析
    position_analysis = None
    position_info = None
    if has_position and current_position > 0 and cost_price > 0:
        position_analysis = analyzer.analyze_position(latest_price, cost_price, current_position, signal_result, data_with_indicators)
        position_info = {
            'profit_loss_pct': position_analysis['profit_loss_pct'],
            'total_cost': position_analysis['total_cost'],
            'position_size': current_position,
            'cost_price': cost_price  # 添加缺失的cost_price字段
        }
    
    # 生成交易决策（考虑持仓情况）
    decision = analyzer.generate_trading_decision(signal_result, data_with_indicators, position_info)
    
    # 计算仓位管理
    position_mgmt = analyzer.calculate_position_management(decision, latest_price)
    
    # 计算止盈止损
    atr = data_with_indicators.iloc[-1]['ATR']
    if pd.isna(atr):
        atr = latest_price * 0.02
    stop_strategy = analyzer.calculate_stop_profit_loss(latest_price, atr)
    
    return data_with_indicators, band_info, signal_result, decision, position_mgmt, stop_strategy, position_analysis

def main():
    # 主标题
    st.markdown('<h1 class="main-header">📈 智策波段交易助手 (BandMaster Pro)</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("📊 分析设置")
        
        # 股票代码输入
        stock_symbol = st.text_input(
            "请输入股票代码",
            value="000001",
            help="输入6位股票代码，如：000001"
        ).strip()
        
        # 分析周期设置
        period = st.selectbox(
            "分析周期",
            options=[60, 100, 150, 200],
            index=1,
            help="选择获取历史数据的天数"
        )
        
        st.markdown("---")
        
        # 仓位管理设置
        st.header("💼 仓位管理")
        
        # 是否有持仓
        has_position = st.checkbox("📊 我有该股票的持仓", value=False)
        
        current_position = 0
        cost_price = 0
        
        if has_position:
            col_pos1, col_pos2 = st.columns(2)
            with col_pos1:
                current_position = st.number_input(
                    "持仓数量(股)",
                    min_value=0,
                    value=1000,
                    step=100,
                    help="您当前持有的股票数量"
                )
            with col_pos2:
                cost_price = st.number_input(
                    "成本价(元)",
                    min_value=0.01,
                    value=10.0,
                    step=0.01,
                    format="%.2f",
                    help="您的平均持仓成本"
                )
        
        # 分析按钮
        analyze_button = st.button("🔍 开始分析", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        # 数据设置
        st.header("⚡ 数据设置")
        
        st.info("📊 当前使用历史数据分析模式，确保数据稳定性")
        
        # 清除缓存按钮
        if st.button("🔄 清除缓存", help="强制刷新所有数据，解决缓存问题"):
            st.cache_data.clear()
            st.success("✅ 缓存已清除，下次分析将获取最新数据")
        
        st.markdown("---")
        
        # 系统信息
        st.markdown("""
        ### 📋 系统说明
        
        **核心功能：**
        - 🎯 智能波段识别
        - 📊 六维信号验证
        - 💰 动态仓位管理
        - ⚠️ 风险控制体系
        
        **三准原则：**
        - ✅ 波段识别准
        - ✅ 买卖点位准  
        - ✅ 仓位控制准
        """)
    
    # 主要内容区域
    if analyze_button and stock_symbol:
        with st.spinner(f"正在分析股票 {stock_symbol}..."):
            try:
                # 加载基础数据（使用缓存）
                with st.spinner("正在获取股票数据..."):
                    data, stock_info, fund_flow = load_basic_stock_data(stock_symbol, period)
                
                if data is None or data.empty:
                    st.error("❌ 获取股票数据失败，请检查股票代码是否正确")
                    return
                
                # 生成数据hash用于缓存控制
                import hashlib
                data_hash = hashlib.md5(f"{stock_symbol}_{period}_{len(data)}".encode()).hexdigest()
                
                # 分析数据（智能缓存：考虑持仓信息变化）
                with st.spinner("正在分析技术指标..."):
                    analysis_result = analyze_stock_cached(
                        stock_symbol, period, has_position, current_position, cost_price, data_hash
                    )
                
                if analysis_result is None:
                    st.error("❌ 技术分析失败，请重试")
                    return
                
                data_with_indicators, band_info, signal_result, decision, position_mgmt, stop_strategy, position_analysis = analysis_result
                
                # 显示数据获取状态
                col_status1, col_status2 = st.columns(2)
                
                with col_status1:
                    st.success("✅ 历史数据获取成功")
                
                with col_status2:
                    if fund_flow is None or fund_flow['main_net_inflow'] == 0:
                        st.info("ℹ️ 资金流向数据不可用")
                    else:
                        st.success("✅ 资金流向数据正常")
                
                # 数据源状态信息
                st.info("📊 **数据源状态：** 历史数据分析模式")
                
                # 创建可视化
                visualizer = StockVisualizer()
                
                # 显示股票基本信息
                st.markdown("## 📊 股票概览")
                
                # 根据是否有持仓显示不同的概览信息
                if has_position and position_analysis:
                    col1, col2, col3, col4, col5 = st.columns(5)
                else:
                    col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    current_price = data.iloc[-1]['close']
                    
                    # 计算历史涨跌幅
                    if len(data) >= 2:
                        prev_close = data.iloc[-2]['close']
                        change_pct = ((current_price - prev_close) / prev_close) * 100
                    else:
                        change_pct = 0
                    
                    # 自定义涨跌幅显示颜色（红色上涨，绿色下跌）
                    if change_pct > 0:
                        delta_display = f"🔴 +{change_pct:.2f}%"
                    elif change_pct < 0:
                        delta_display = f"🟢 {change_pct:.2f}%"
                    else:
                        delta_display = f"⚪ {change_pct:.2f}%"
                    
                    st.metric(
                        label="当前价格",
                        value=f"￥{current_price:.2f}",
                        delta=delta_display
                    )
                
                with col2:
                    st.metric(
                        label="股票名称",
                        value=stock_info.get('name', '未知')
                    )
                
                with col3:
                    st.metric(
                        label="所属行业",
                        value=stock_info.get('industry', '未知')
                    )
                
                with col4:
                    st.metric(
                        label="信号强度",
                        value=f"{signal_result['signal_count']}/{signal_result['total_signals']}",
                        delta=f"{decision['confidence']}置信度"
                    )
                
                # 如果有持仓，显示盈亏信息
                if has_position and position_analysis:
                    with col5:
                        profit_loss_pct = position_analysis['profit_loss_pct']
                        profit_loss = position_analysis['profit_loss']
                        
                        # 自定义盈亏显示颜色（红色盈利，绿色亏损）
                        if profit_loss_pct > 0:
                            delta_display = f"🔴 +{profit_loss_pct:.2f}%"
                        elif profit_loss_pct < 0:
                            delta_display = f"🟢 {profit_loss_pct:.2f}%"
                        else:
                            delta_display = f"⚪ {profit_loss_pct:.2f}%"
                        
                        st.metric(
                            label="持仓盈亏",
                            value=f"￥{profit_loss:,.0f}",
                            delta=delta_display
                        )
                
                # 显示图表
                st.markdown("## 📈 技术分析图表")
                chart = visualizer.create_stock_chart(data_with_indicators, stock_info, signal_result, band_info)
                st.plotly_chart(chart, use_container_width=True)
                
                # 显示分析结果 - 重新设计布局
                latest_price = data_with_indicators.iloc[-1]['close']
                support_level = data_with_indicators['close'].quantile(0.2)
                resistance_level = data_with_indicators['close'].quantile(0.8)
                
                # 第一行：核心决策和波段位置
                st.markdown("## 🎯 核心分析结果")
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    # 操作决策
                    action_color = "🟢" if "买入" in decision['decision'] or "加仓" in decision['decision'] else "🔴" if "卖出" in decision['decision'] or "止损" in decision['decision'] else "🟡"
                    st.success(f"""
**📊 操作决策：**

{action_color} **{decision['decision']}**
**置信度：** {decision['confidence']}%
**建议仓位：** {decision['position_ratio']*100:.0f}%

**🎯 目标价位：** ￥{decision['target_price']:.2f}
**⛔ 止损价位：** ￥{decision['stop_loss']:.2f}
**⏰ 持有周期：** {decision['holding_period']}
                    """)
                
                with col2:
                    # 波段位置分析
                    st.info(f"""
**📈 波段位置分析：**

**当前位置：** {band_info['position']}
**位置描述：** {band_info['position_description']}
**指导建议：** {band_info['guidance']}

**波段类型：** {band_info['type']}
**预期周期：** {band_info['period_range']}
**位置百分比：** {band_info.get('position_percent', 0):.1f}%
                    """)
                
                with col3:
                    # 信号验证汇总
                    signal_count = signal_result['signal_count']
                    total_signals = signal_result['total_signals']
                    signal_percent = (signal_count / total_signals) * 100
                    
                    signal_color = "🟢" if signal_percent >= 80 else "🟡" if signal_percent >= 60 else "🔴"
                    st.warning(f"""
**🔍 信号验证汇总：**

{signal_color} **{signal_count}/{total_signals}** ({signal_percent:.0f}%)

**趋势方向：** {'✅' if signal_result['signals']['trend_direction']['status'] else '❌'}
**动量强度：** {'✅' if signal_result['signals']['momentum_strength']['status'] else '❌'}
**量能配合：** {'✅' if signal_result['signals']['volume_cooperation']['status'] else '❌'}
**形态确认：** {'✅' if signal_result['signals']['pattern_confirmation']['status'] else '❌'}
**市场环境：** {'✅' if signal_result['signals']['market_environment']['status'] else '❌'}
                    """)
                
                # 第二行：持仓信息和风险管理
                st.markdown("## 💼 持仓管理与风险控制")
                col4, col5 = st.columns([1, 1])
                
                with col4:
                    # 持仓信息（如果有持仓）
                    if has_position and position_analysis:
                        profit_loss_pct = position_analysis['profit_loss_pct']
                        profit_loss = position_analysis['profit_loss']
                        
                        # 自定义盈亏显示颜色
                        if profit_loss_pct > 0:
                            delta_display = f"🔴 +{profit_loss_pct:.2f}%"
                        elif profit_loss_pct < 0:
                            delta_display = f"🟢 {profit_loss_pct:.2f}%"
                        else:
                            delta_display = f"⚪ {profit_loss_pct:.2f}%"
                        
                        st.info(f"""
**📊 持仓状态分析：**

**持仓数量：** {current_position:,}股
**成本价格：** ￥{cost_price:.2f}
**当前价格：** ￥{latest_price:.2f}
**持仓状态：** {position_analysis['position_status']}
**盈亏情况：** {delta_display} (￥{profit_loss:,.0f})
**风险等级：** {position_analysis['risk_level']}
**趋势强度：** {position_analysis['trend_strength']}

**操作建议：**
根据当前持仓状态和信号强度，建议{position_analysis.get('suggestion', '谨慎操作')}
                        """)
                    else:
                        st.info(f"""
**📊 持仓状态：**
暂无持仓信息

**建议操作：**
根据当前信号强度，建议{decision['position_ratio']*100:.0f}%仓位操作
目标价位：￥{decision['target_price']:.2f}
止损价位：￥{decision['stop_loss']:.2f}
                        """)
                
                with col5:
                    # 风险管理
                    st.warning(f"""
**⚠️ 风险控制要点：**

**🎯 关键价位：**
- 目标价位：￥{decision['target_price']:.2f}
- 止损价位：￥{decision['stop_loss']:.2f}
- 移动止损：￥{stop_strategy['trailing_stop']:.2f}
- 紧急止损：￥{stop_strategy['emergency_stop']:.2f}

**📊 仓位建议：**
- 建议仓位：{position_mgmt['suggested_position']:.0f}%
- 底仓配置：{position_mgmt['bottom_position']*100:.0f}%
- 突破加仓：{position_mgmt['breakout_add']*100:.0f}%
- 回调补仓：{position_mgmt['pullback_add']*100:.0f}%
- 机动T+0：{position_mgmt['flexible_trade']*100:.0f}%

**⏰ 时间控制：**
- 持有周期：{decision['holding_period']}
- 时间止损：{stop_strategy['time_stop']}日
- 建议操作：{decision['decision']}
                    """)
                
                # 第三行：技术指标和支撑压力位
                st.markdown("## 📊 技术指标与关键位置")
                col6, col7, col8 = st.columns([1, 1, 1])
                
                with col6:
                    # 关键价格位置
                    st.info(f"""
**📍 关键价格位置：**

**当前价格：** ￥{latest_price:.2f}
**支撑位：** ￥{support_level:.2f}
**压力位：** ￥{resistance_level:.2f}
**20日高点：** ￥{band_info.get('high_20', 0):.2f}
**20日低点：** ￥{band_info.get('low_20', 0):.2f}

**价格区间：** ￥{band_info.get('low_20', 0):.2f} - ￥{band_info.get('high_20', 0):.2f}

**位置分析：**
当前位置在20日区间{band_info.get('position_percent', 0):.1f}%处
                    """)
                
                with col7:
                    # 主要技术指标
                    latest = data_with_indicators.iloc[-1]
                    st.info(f"""
**📈 主要技术指标：**

**RSI：** {latest['RSI']:.1f}
**MACD：** {latest['MACD']:.3f}
**ADX：** {latest['ADX']:.1f}
**ATR：** {latest['ATR']:.3f}
**量比：** {latest['Volume_Ratio']:.1f}

**布林带位置：** {((latest['close'] - latest['BB_lower']) / (latest['BB_upper'] - latest['BB_lower']) * 100):.1f}%

**指标解读：**
RSI {'超买' if latest['RSI'] > 75 else '超卖' if latest['RSI'] < 25 else '正常'}
MACD {'金叉' if latest['MACD'] > 0 else '死叉'}
                    """)
                
                with col8:
                    # 止盈止损设置
                    st.info(f"""
**🎯 止盈止损设置：**

**阶梯止盈：**
- 15%收益：￥{stop_strategy['step_profit']['15%']:.2f}
- 25%收益：￥{stop_strategy['step_profit']['25%']:.2f}
- 40%收益：￥{stop_strategy['step_profit']['40%']:.2f}

**止损策略：**
- 移动止损：￥{stop_strategy['trailing_stop']:.2f}
- 时间止损：{stop_strategy['time_stop']}日
- 紧急止损：￥{stop_strategy['emergency_stop']:.2f}

**风险提示：**
严格执行止损，控制单笔损失在5%以内
                    """)
                
                # 详细信号分析
                st.markdown("## 🔍 详细信号分析")
                
                # 信号说明
                fund_data_available = signal_result['signals']['fund_verification'].get('data_available', True)
                signal_count_text = "五维信号" if not fund_data_available else "六维信号"
                
                signal_explanation = f"""
                **📋 {signal_count_text}说明：**
                - **趋势方向**：20/60日均线多头排列，判断中期趋势
                - **动量强度**：RSI指标在45-75区间，判断超买超卖
                - **量能配合**：成交量大于5日均量120%，判断资金活跃度
                """
                
                if fund_data_available:
                    signal_explanation += "- **资金验证**：主力资金净流入，判断机构态度\n"
                
                signal_explanation += """
                - **形态确认**：价格突破重要阻力位，判断技术形态
                - **市场环境**：ADX指标大于25，判断趋势强度
                """
                
                if not fund_data_available:
                    signal_explanation += "\n⚠️ **注意**：资金流向数据暂时不可用，已自动调整为五维信号分析"
                
                st.info(signal_explanation)
                
                signals_df = []
                for key, signal in signal_result['signals'].items():
                    signal_names = {
                        'trend_direction': '趋势方向',
                        'momentum_strength': '动量强度',
                        'volume_cooperation': '量能配合',
                        'fund_verification': '资金验证',
                        'pattern_confirmation': '形态确认',
                        'market_environment': '市场环境'
                    }
                    
                    # 处理强度值，确保是字符串格式
                    strength_value = signal.get('strength', signal.get('value', signal.get('ratio', signal.get('net_inflow', signal.get('adx_value', None)))))
                    if strength_value is not None:
                        try:
                            # 如果是数字，格式化为字符串
                            if isinstance(strength_value, (int, float)):
                                if key == 'momentum_strength':
                                    strength_str = f"RSI: {strength_value:.1f}"
                                elif key == 'volume_cooperation':
                                    strength_str = f"量比: {strength_value:.1f}"
                                elif key == 'fund_verification':
                                    strength_str = f"净流入: {strength_value:,.0f}万"
                                elif key == 'market_environment':
                                    strength_str = f"ADX: {strength_value:.1f}"
                                else:
                                    strength_str = f"{strength_value:.2f}" if isinstance(strength_value, float) else str(strength_value)
                            else:
                                strength_str = str(strength_value)
                        except:
                            strength_str = "未知"
                    else:
                        strength_str = "未知"
                    
                    # 生成更详细的状态描述
                    status_text = "✅ 符合条件" if signal['status'] else "❌ 不符合条件"
                    if key == 'trend_direction':
                        status_text = "✅ 多头排列" if signal['status'] else "❌ 空头排列"
                    elif key == 'momentum_strength':
                        status_text = "✅ 理想区间" if signal['status'] else "❌ 过热/过冷"
                    elif key == 'volume_cooperation':
                        status_text = "✅ 量能放大" if signal['status'] else "❌ 量能不足"
                    elif key == 'fund_verification':
                        if signal.get('data_available', True):
                            status_text = "✅ 资金流入" if signal['status'] else "❌ 资金流出"
                        else:
                            status_text = "⚠️ 数据不可用"
                    elif key == 'pattern_confirmation':
                        status_text = "✅ 形态突破" if signal['status'] else "❌ 无突破"
                    elif key == 'market_environment':
                        status_text = "✅ 趋势明确" if signal['status'] else "❌ 震荡整理"
                    
                    signals_df.append({
                        '信号类型': signal_names.get(key, key),
                        '状态': status_text,
                        '具体数值': strength_str,
                        '详细说明': signal['description']
                    })
                
                st.dataframe(
                    pd.DataFrame(signals_df),
                    use_container_width=True,
                    hide_index=True
                )
                
                # 技术指标数据表
                with st.expander("📊 查看详细技术指标数据"):
                    display_columns = ['close', 'MA5', 'MA10', 'MA20', 'MA60', 'RSI', 'MACD', 'Volume_Ratio']
                    available_columns = [col for col in display_columns if col in data_with_indicators.columns]
                    
                    # 处理数据，确保没有导致Arrow转换问题的值
                    display_data = data_with_indicators[available_columns].tail(10).copy()
                    
                    # 将所有NaN值替换为0，并确保数据类型正确
                    display_data = display_data.fillna(0).round(3)
                    
                    # 确保所有列都是数字类型
                    for col in display_data.columns:
                        try:
                            display_data[col] = pd.to_numeric(display_data[col], errors='coerce').fillna(0)
                        except:
                            pass
                    
                    st.dataframe(
                        display_data,
                        use_container_width=True
                    )
                
                # 复制结果功能
                st.markdown("---")
                st.markdown("## 📋 复制分析结果")
                
                # 生成分析结果文本
                def generate_analysis_text():
                    # 计算关键价格位置
                    support_level = data_with_indicators['close'].quantile(0.2)
                    resistance_level = data_with_indicators['close'].quantile(0.8)
                    latest = data_with_indicators.iloc[-1]
                    
                    text = f"""
📈 智策波段交易助手 - 分析报告
股票代码：{stock_symbol}
股票名称：{stock_info.get('name', '未知')}
分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
分析周期：{period}天

📊 基本信息：
当前价格：￥{current_price:.2f}
涨跌幅：{change_pct:.2f}%
所属行业：{stock_info.get('industry', '未知')}

🎯 波段分析：
波段类型：{band_info['type']}
预期周期：{band_info['period_range']}
当前位置：{band_info['position']}
位置描述：{band_info['position_description']}
指导建议：{band_info['guidance']}
位置百分比：{band_info.get('position_percent', 0):.1f}%

📈 操作建议：
{decision['decision']}
置信度：{decision['confidence']}%
建议仓位：{decision['position_ratio']*100:.0f}%
目标价位：￥{decision['target_price']:.2f}
止损价位：￥{decision['stop_loss']:.2f}
建议持有：{decision['holding_period']}

💼 仓位管理：
建议仓位：{position_mgmt['suggested_position']:.0f}%
底仓配置：{position_mgmt['bottom_position']*100:.0f}%
回调补仓：{position_mgmt['pullback_add']*100:.0f}%
突破加仓：{position_mgmt['breakout_add']*100:.0f}%
机动T+0：{position_mgmt['flexible_trade']*100:.0f}%

🛡️ 止盈止损：
阶梯止盈15%：￥{stop_strategy['step_profit']['15%']:.2f}
阶梯止盈25%：￥{stop_strategy['step_profit']['25%']:.2f}
阶梯止盈40%：￥{stop_strategy['step_profit']['40%']:.2f}
移动止损：￥{stop_strategy['trailing_stop']:.2f}
时间止损：{stop_strategy['time_stop']}日
紧急止损：￥{stop_strategy['emergency_stop']:.2f}

📍 关键价格位置：
当前价格：￥{current_price:.2f}
支撑位：￥{support_level:.2f}
压力位：￥{resistance_level:.2f}
20日高点：￥{band_info.get('high_20', 0):.2f}
20日低点：￥{band_info.get('low_20', 0):.2f}
价格区间：￥{band_info.get('low_20', 0):.2f} - ￥{band_info.get('high_20', 0):.2f}

📈 主要技术指标：
RSI：{latest['RSI']:.1f}
MACD：{latest['MACD']:.3f}
ADX：{latest['ADX']:.1f}
ATR：{latest['ATR']:.3f}
量比：{latest['Volume_Ratio']:.1f}
布林带位置：{((latest['close'] - latest['BB_lower']) / (latest['BB_upper'] - latest['BB_lower']) * 100):.1f}%

🔍 信号验证汇总：
信号强度：{signal_result['signal_count']}/{signal_result['total_signals']} ({(signal_result['signal_count'] / signal_result['total_signals']) * 100:.0f}%)
趋势方向：{'✅' if signal_result['signals']['trend_direction']['status'] else '❌'}
动量强度：{'✅' if signal_result['signals']['momentum_strength']['status'] else '❌'}
量能配合：{'✅' if signal_result['signals']['volume_cooperation']['status'] else '❌'}
形态确认：{'✅' if signal_result['signals']['pattern_confirmation']['status'] else '❌'}
市场环境：{'✅' if signal_result['signals']['market_environment']['status'] else '❌'}

🔍 详细信号验证：
"""
                    
                    # 添加信号验证详情
                    for key, signal in signal_result['signals'].items():
                        signal_names = {
                            'trend_direction': '趋势方向',
                            'momentum_strength': '动量强度',
                            'volume_cooperation': '量能配合',
                            'fund_verification': '资金验证',
                            'pattern_confirmation': '形态确认',
                            'market_environment': '市场环境'
                        }
                        
                        # 处理强度值显示
                        strength_value = signal.get('strength', signal.get('value', signal.get('ratio', signal.get('net_inflow', signal.get('adx_value', None)))))
                        if strength_value is not None:
                            try:
                                if isinstance(strength_value, (int, float)):
                                    if key == 'momentum_strength':
                                        strength_str = f"RSI: {strength_value:.1f}"
                                    elif key == 'volume_cooperation':
                                        strength_str = f"量比: {strength_value:.1f}"
                                    elif key == 'fund_verification':
                                        strength_str = f"净流入: {strength_value:,.0f}万"
                                    elif key == 'market_environment':
                                        strength_str = f"ADX: {strength_value:.1f}"
                                    else:
                                        strength_str = f"{strength_value:.2f}" if isinstance(strength_value, float) else str(strength_value)
                                else:
                                    strength_str = str(strength_value)
                            except:
                                strength_str = "未知"
                        else:
                            strength_str = "未知"
                        
                        # 处理资金验证信号的特殊情况
                        if key == 'fund_verification' and not signal.get('data_available', True):
                            status = "⚠️ 数据不可用"
                        else:
                            status = "✅ 符合条件" if signal['status'] else "❌ 不符合条件"
                        
                        text += f"{signal_names.get(key, key)}：{status} - {strength_str} - {signal['description']}\n"
                    
                    # 如果有持仓信息，添加持仓分析
                    if has_position and position_analysis:
                        profit_loss_pct = position_analysis['profit_loss_pct']
                        profit_loss = position_analysis['profit_loss']
                        
                        # 自定义盈亏显示
                        if profit_loss_pct > 0:
                            delta_display = f"+{profit_loss_pct:.2f}%"
                        elif profit_loss_pct < 0:
                            delta_display = f"{profit_loss_pct:.2f}%"
                        else:
                            delta_display = f"{profit_loss_pct:.2f}%"
                        
                        text += f"""
💼 持仓分析：
持仓数量：{current_position:,}股
成本价格：￥{cost_price:.2f}
当前价格：￥{current_price:.2f}
持仓状态：{position_analysis['position_status']}
盈亏情况：{delta_display} (￥{profit_loss:,.0f})
风险等级：{position_analysis['risk_level']}
趋势强度：{position_analysis['trend_strength']}
"""
                    
                    text += """
⚠️ 风险提示：
本分析基于技术指标，仅供参考，投资有风险，决策需谨慎。
股市有风险，投资需谨慎！
"""
                    
                    return text
                
                # 生成分析文本
                analysis_text = generate_analysis_text()
                
                # 显示分析结果预览
                st.text_area(
                    "分析结果预览",
                    value=analysis_text,
                    height=400,
                    disabled=True,
                    help="请手动选择上方内容，然后按 Ctrl+C (Mac: Cmd+C) 复制到剪贴板"
                )
                

                
                # 下载按钮（可选）
                if st.button("💾 下载分析报告", type="secondary", use_container_width=True):
                    # 创建下载链接
                    import base64
                    
                    # 编码文本内容
                    b64 = base64.b64encode(analysis_text.encode()).decode()
                    
                    # 创建下载链接
                    href = f'<a href="data:file/txt;base64,{b64}" download="股票分析报告_{stock_symbol}_{datetime.now().strftime("%Y%m%d_%H%M")}.txt">📥 点击下载分析报告</a>'
                    st.markdown(href, unsafe_allow_html=True)
                
                # 免责声明
                st.markdown("---")
                st.warning("""
                ⚠️ **重要风险提示**：
                
                本系统分析结果基于历史数据与量化模型，不构成任何投资建议。
                使用者需独立承担投资决策风险，建议结合个人风险承受能力谨慎参考。
                
                股市有风险，投资需谨慎！
                """)
                
            except Exception as e:
                st.error(f"❌ 分析过程中出现错误：{str(e)}")
                st.info("💡 请尝试以下解决方案：\n1. 检查股票代码格式\n2. 检查网络连接\n3. 稍后重试")
    
    elif not stock_symbol:
        # 显示欢迎页面
        st.markdown("""
        ## 🚀 欢迎使用智策波段交易助手！
        
        ### 📋 使用说明：
        1. 在左侧输入6位股票代码（如：000001）
        2. 选择分析周期
        3. 点击"开始分析"按钮
        4. 查看完整的波段分析报告
        
        ### 🎯 系统特色：
        - **智能波段识别**：多周期协同分析
        - **六维信号验证**：趋势、动量、量能、资金、形态、环境
        - **精准买卖点**：基于量化模型的决策矩阵
        - **动态仓位管理**：底仓+加仓+补仓+T+0策略
        - **完整风控体系**：止盈、止损、时间、紧急四重保护
        
        ### 🔧 技术架构：
        - 数据源：AkShare实时数据
        - 技术分析：TA-Lib专业指标库
        - 可视化：Plotly交互式图表
        - 框架：Streamlit Web应用
        """)
        
        # 显示示例图片或者演示
        st.markdown("### 📊 分析示例")
        st.info("输入股票代码开始您的波段交易分析之旅！")

if __name__ == "__main__":
    main() 