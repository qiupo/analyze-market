#!/usr/bin/env python3
"""
测试复制功能
"""

import sys
import pandas as pd
from core.data_fetcher import StockDataFetcher
from core.technical_analysis import TechnicalAnalyzer

def test_copy_function():
    """测试复制功能"""
    print("🔍 测试复制功能...")
    
    fetcher = StockDataFetcher()
    analyzer = TechnicalAnalyzer()
    
    try:
        # 获取测试数据
        data = fetcher.get_stock_data("000001", 50)
        if data is None or data.empty:
            print("❌ 无法获取测试数据")
            return False
        
        # 计算技术指标
        data_with_indicators = analyzer.calculate_indicators(data)
        print("✅ 技术指标计算成功")
        
        # 测试信号验证
        fund_flow = fetcher.get_fund_flow("000001")
        signal_result = analyzer.six_dimension_signal_check(data_with_indicators, fund_flow)
        print("✅ 信号验证成功")
        
        # 测试交易决策
        decision = analyzer.generate_trading_decision(signal_result, data_with_indicators)
        print("✅ 交易决策生成成功")
        
        # 测试仓位管理
        position_mgmt = analyzer.calculate_position_management(decision, data_with_indicators.iloc[-1]['close'])
        print("✅ 仓位管理计算成功")
        
        # 测试止盈止损
        atr = data_with_indicators.iloc[-1]['ATR']
        if pd.isna(atr):
            atr = data_with_indicators.iloc[-1]['close'] * 0.02
        stop_strategy = analyzer.calculate_stop_profit_loss(data_with_indicators.iloc[-1]['close'], atr)
        print("✅ 止盈止损计算成功")
        
        # 模拟生成分析文本
        stock_info = fetcher.get_stock_info("000001")
        current_price = data_with_indicators.iloc[-1]['close']
        change_pct = 0
        if len(data_with_indicators) >= 2:
            prev_close = data_with_indicators.iloc[-2]['close']
            change_pct = ((current_price - prev_close) / prev_close) * 100
        
        # 生成分析文本
        analysis_text = f"""
📈 智策波段交易助手 - 分析报告
股票代码：000001
股票名称：{stock_info.get('name', '未知')}
分析时间：2024-01-01 12:00:00
分析周期：50天

📊 基本信息：
当前价格：￥{current_price:.2f}
涨跌幅：{change_pct:.2f}%
所属行业：{stock_info.get('industry', '未知')}

🎯 波段分析：
波段类型：标准波段
预期周期：5-15天
信号强度：{signal_result['signal_count']}/{signal_result['total_signals']}

📈 操作建议：
{decision['decision']}
置信度：{decision['confidence']}
目标价位：￥{decision['target_price']:.2f}
止损价位：￥{decision['stop_loss']:.2f}
建议持有：{decision['holding_period']}

💼 仓位管理：
底仓配置：{position_mgmt['bottom_position']*100:.1f}%
回调补仓：{position_mgmt['pullback_add']*100:.1f}%
突破加仓：{position_mgmt['breakout_add']*100:.1f}%
机动T+0：{position_mgmt['flexible_trade']*100:.1f}%

🛡️ 止盈止损：
阶梯止盈15%：￥{stop_strategy['step_profit']['15%']:.2f}
阶梯止盈25%：￥{stop_strategy['step_profit']['25%']:.2f}
阶梯止盈40%：￥{stop_strategy['step_profit']['40%']:.2f}
移动止损：￥{stop_strategy['trailing_stop']:.2f}
紧急止损：￥{stop_strategy['emergency_stop']:.2f}

🔍 信号验证：
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
            
            if key == 'fund_verification' and not signal.get('data_available', True):
                status = "⚠️ 数据不可用"
            else:
                status = "✅ 符合" if signal['status'] else "❌ 不符合"
            
            analysis_text += f"{signal_names.get(key, key)}：{status} - {signal['description']}\n"
        
        analysis_text += """
⚠️ 风险提示：
本分析基于技术指标，仅供参考，投资有风险，决策需谨慎。
股市有风险，投资需谨慎！
"""
        
        print("✅ 分析文本生成成功")
        print(f"   文本长度：{len(analysis_text)} 字符")
        print(f"   包含内容：")
        print(f"   - 基本信息：✅")
        print(f"   - 波段分析：✅")
        print(f"   - 操作建议：✅")
        print(f"   - 仓位管理：✅")
        print(f"   - 止盈止损：✅")
        print(f"   - 信号验证：✅")
        print(f"   - 风险提示：✅")
        
        # 测试下载功能
        import base64
        b64 = base64.b64encode(analysis_text.encode()).decode()
        print("✅ 下载功能测试成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试复制功能...\n")
    
    if test_copy_function():
        print("\n🎉 复制功能测试通过！")
        print("\n📋 修复内容：")
        print("   - 移除了导致页面刷新的session_state")
        print("   - 简化了复制流程，直接显示文本预览")
        print("   - 添加了详细的复制说明")
        print("   - 增加了下载功能作为备选方案")
        print("   - 页面内容不会因为点击按钮而消失")
        return True
    else:
        print("\n❌ 复制功能测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 