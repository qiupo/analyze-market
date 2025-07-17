"""
智策波段交易助手配置文件
BandMaster Pro Configuration
"""

# 应用配置
APP_CONFIG = {
    'title': '智策波段交易助手',
    'subtitle': 'BandMaster Pro',
    'version': 'V1.0',
    'port': 8501,
    'cache_ttl': 300,  # 缓存时间（秒）
}

# 数据获取配置
DATA_CONFIG = {
    'default_period': 100,  # 默认获取天数
    'max_period': 500,      # 最大获取天数
    'min_period': 30,       # 最小获取天数
    'retry_times': 3,       # 重试次数
    'timeout': 30,          # 超时时间（秒）
}

# 技术分析参数
TECHNICAL_CONFIG = {
    # 移动平均线参数
    'ma_periods': [5, 10, 20, 60],
    'ema_periods': [20, 60],
    
    # 技术指标参数
    'rsi_period': 14,
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'rsi_ideal_min': 45,
    'rsi_ideal_max': 75,
    
    # MACD参数
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    
    # 布林带参数
    'bb_period': 20,
    'bb_std': 2,
    
    # ADX参数
    'adx_period': 14,
    'adx_trend_threshold': 25,
    'adx_strong_trend': 30,
    
    # ATR参数
    'atr_period': 14,
    
    # KDJ参数
    'kdj_period': 9,
    'kdj_m1': 3,
    'kdj_m2': 3,
    
    # 成交量参数
    'volume_ma_period': 5,
    'volume_amplify_threshold': 1.2,  # 成交量放大阈值
}

# 波段识别配置
BAND_CONFIG = {
    # 波段类型阈值
    'micro_band': {
        'volatility_threshold': 0.4,
        'volume_ratio_threshold': 1.5,
        'period_range': '15-30分钟'
    },
    'short_band': {
        'bb_squeeze_ratio': 0.8,
        'period_range': '1-3天'
    },
    'standard_band': {
        'ma_slope_threshold': 30,  # 度数
        'period_range': '5-15天'
    },
    'trend_band': {
        'adx_threshold': 30,
        'ma_alignment_required': True,
        'period_range': '15-30天'
    }
}

# 信号验证配置
SIGNAL_CONFIG = {
    # 六维信号权重
    'signal_weights': {
        'trend_direction': 1.0,
        'momentum_strength': 1.0,
        'volume_cooperation': 1.0,
        'fund_verification': 1.0,
        'pattern_confirmation': 1.0,
        'market_environment': 1.0
    },
    
    # 信号阈值
    'trend_alignment_required': True,
    'rsi_range': (45, 75),
    'volume_threshold': 1.2,
    'fund_inflow_threshold': 0,
    'adx_market_threshold': 25,
}

# 交易决策配置
DECISION_CONFIG = {
    # 决策矩阵
    'decision_matrix': {
        'heavy_buy': {
            'min_signals': 5,
            'position_ratio': 0.75,
            'holding_period': '5-15天',
            'confidence': '高',
            'target_multiplier': 1.15,
            'stop_loss_atr': 2.0
        },
        'standard_buy': {
            'min_signals': 3,
            'position_ratio': 0.45,
            'holding_period': '3-7天',
            'confidence': '中',
            'target_multiplier': 1.08,
            'stop_loss_atr': 1.5
        },
        'light_buy': {
            'min_signals': 2,
            'position_ratio': 0.15,
            'holding_period': '1-3天',
            'confidence': '低',
            'target_multiplier': 1.05,
            'stop_loss_atr': 1.0
        },
        'hold': {
            'min_signals': 0,
            'position_ratio': 0.0,
            'holding_period': '-',
            'confidence': '观望',
            'target_multiplier': 1.0,
            'stop_loss_atr': 0
        }
    }
}

# 仓位管理配置
POSITION_CONFIG = {
    # 仓位分配比例
    'allocation': {
        'bottom_position': 0.5,    # 50%底仓
        'breakout_add': 0.25,      # 25%突破加仓
        'pullback_add': 0.15,      # 15%回调补仓
        'flexible_trade': 0.1      # 10%机动T+0
    },
    
    # 单股风险限额
    'single_stock_limit': 0.3,     # 单股不超过总仓位30%
    'sector_limit': 0.25,          # 同行业不超过25%
    
    # 黑名单规则
    'blacklist_rules': {
        'st_stocks': True,          # 排除ST股票
        'low_volatility': 0.03,     # 排除5日振幅<3%的股票
        'min_volume': 1000000       # 最小成交量要求
    }
}

# 风险控制配置
RISK_CONFIG = {
    # 止盈策略
    'take_profit': {
        'step_profits': [0.15, 0.25, 0.40],  # 阶梯止盈点
        'step_reduce_ratio': 1/3,              # 每次减持比例
    },
    
    # 止损策略
    'stop_loss': {
        'trailing_stop_pct': 0.07,    # 7%移动止损
        'time_stop_days': 5,           # 5日时间止损
        'emergency_stop_atr': 2.0,     # 紧急止损ATR倍数
    },
    
    # 系统级风控
    'system_risk': {
        'data_freshness_threshold': 300,  # 数据新鲜度阈值（秒）
        'volatility_threshold': 0.05,     # 波动率熔断阈值
        'max_drawdown': 0.15,             # 最大回撤限制
    }
}

# 可视化配置
VISUAL_CONFIG = {
    # 颜色主题
    'colors': {
        'bullish': '#00C853',      # 上涨绿色
        'bearish': '#FF1744',      # 下跌红色
        'neutral': '#757575',      # 中性灰色
        'volume': '#1976D2',       # 成交量蓝色
        'ma_colors': ['#FF9800', '#2196F3', '#9C27B0', '#4CAF50'],  # 均线颜色
        'background': '#FAFAFA'     # 背景色
    },
    
    # 图表配置
    'chart': {
        'height': 800,             # 图表高度
        'subplot_rows': 4,         # 子图行数
        'subplot_spacing': 0.02,   # 子图间距
        'show_legend': True,       # 显示图例
        'template': 'plotly_white' # 图表主题
    },
    
    # 指标显示
    'indicators': {
        'show_ma': True,           # 显示移动平均线
        'show_bollinger': True,    # 显示布林带
        'show_volume_ma': True,    # 显示成交量均线
        'rsi_levels': [30, 50, 70], # RSI关键水平线
    }
}

# 提示信息配置
MESSAGES = {
    'risk_warning': """
⚠️ **重要风险提示**：
本系统分析结果基于历史数据与量化模型，不构成任何投资建议。
使用者需独立承担投资决策风险，建议结合个人风险承受能力谨慎参考。
股市有风险，投资需谨慎！
    """,
    
    'data_error': "❌ 获取股票数据失败，请检查股票代码是否正确",
    'network_error': "🌐 网络连接异常，请检查网络状态后重试",
    'analysis_error': "📊 分析过程中出现错误，请稍后重试",
    
    'success_tips': """
💡 分析完成！您可以：
1. 查看技术分析图表了解趋势
2. 参考操作建议制定策略
3. 关注风险管理提示
4. 结合个人情况理性决策
    """
} 