import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockDataFetcher:
    """股票数据获取器"""
    
    def __init__(self):
        self.ak = ak
    
    def get_stock_data(self, symbol, period=100):
        """
        获取股票历史数据
        
        Args:
            symbol: 股票代码 (如: '000001')
            period: 获取天数
            
        Returns:
            DataFrame: 包含OHLCV数据
        """
        try:
            # 获取股票历史数据
            stock_data = ak.stock_zh_a_hist(
                symbol=symbol, 
                period="daily", 
                start_date=(datetime.now() - timedelta(days=period*2)).strftime("%Y%m%d"),
                end_date=datetime.now().strftime("%Y%m%d"),
                adjust="qfq"
            )
            
            if stock_data.empty:
                return None
                
            # 动态处理列名
            print(f"获取到的列数: {len(stock_data.columns)}")
            print(f"列名: {list(stock_data.columns)}")
            
            # 根据实际列数处理 - 现在我们知道有12列
            # 列名: ['日期', '股票代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
            if len(stock_data.columns) >= 7:
                # 选择需要的列：日期、开盘、收盘、最高、最低、成交量
                # 跳过股票代码列，选择第0,2,3,4,5,6列
                selected_data = stock_data.iloc[:, [0, 2, 3, 4, 5, 6]].copy()
                selected_data.columns = ['date', 'open', 'close', 'high', 'low', 'volume']
                stock_data = selected_data
            elif len(stock_data.columns) >= 6:
                # 如果是6列，按原来的逻辑处理
                stock_data = stock_data.iloc[:, :6]
                stock_data.columns = ['date', 'open', 'close', 'high', 'low', 'volume']
            else:
                # 如果列数不够，使用原始列名
                stock_data.columns = [f'col_{i}' for i in range(len(stock_data.columns))]
                
            stock_data['date'] = pd.to_datetime(stock_data.iloc[:, 0])
            stock_data.set_index('date', inplace=True)
            
            # 重新排列列顺序并确保数据类型
            try:
                columns_needed = ['open', 'high', 'low', 'close', 'volume']
                if 'high' not in stock_data.columns and 'close' in stock_data.columns:
                    # 如果列名不匹配，尝试重新映射
                    available_cols = [col for col in stock_data.columns if col != 'date']
                    if len(available_cols) >= 5:
                        stock_data.columns = ['open', 'close', 'high', 'low', 'volume'][:len(available_cols)]
                        # 调整为正确顺序
                        stock_data = stock_data[['open', 'high', 'low', 'close', 'volume'][:len(available_cols)]]
                
                stock_data = stock_data[columns_needed].astype(float)
            except Exception as e:
                print(f"列处理错误: {e}")
                # 如果还是有问题，使用最基本的处理
                numeric_cols = stock_data.select_dtypes(include=[np.number]).columns[:5]
                stock_data = stock_data[numeric_cols]
                stock_data.columns = ['open', 'high', 'low', 'close', 'volume'][:len(numeric_cols)]
            
            return stock_data.tail(period)
            
        except Exception as e:
            print(f"获取股票数据失败: {e}")
            return None
    
    def get_stock_info(self, symbol):
        """获取股票基本信息"""
        try:
            # 设置超时
            import socket
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(10)  # 10秒超时
            
            try:
                # 获取股票信息
                stock_info = ak.stock_individual_info_em(symbol=symbol)
                
                if stock_info.empty:
                    return self._get_default_stock_info(symbol)
                
                # 提取信息
                info_dict = self._get_default_stock_info(symbol)
                
                for _, row in stock_info.iterrows():
                    item = row.get('item', '')
                    value = row.get('value', '')
                    
                    if '股票简称' in item or '名称' in item:
                        info_dict['name'] = value
                    elif '所属行业' in item or '行业' in item:
                        info_dict['industry'] = value
                    elif '总市值' in item:
                        try:
                            info_dict['market_cap'] = float(value.replace('亿', '').replace('万', ''))
                        except:
                            pass
                    elif '市盈率' in item:
                        try:
                            info_dict['pe_ratio'] = float(value)
                        except:
                            pass
                    elif '市净率' in item:
                        try:
                            info_dict['pb_ratio'] = float(value)
                        except:
                            pass
                
                return info_dict
                
            finally:
                socket.setdefaulttimeout(original_timeout)
            
        except Exception as e:
            print(f"获取股票信息失败: {e}")
            return self._get_default_stock_info(symbol)
    
    def _get_default_stock_info(self, symbol):
        """返回默认的股票信息"""
        return {
            'name': f'股票{symbol}',
            'industry': '未知',
            'market_cap': 0,
            'pe_ratio': 0,
            'pb_ratio': 0
        }
    
    def get_fund_flow(self, symbol):
        """获取资金流向数据"""
        try:
            # 设置超时和重试机制
            import socket
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(10)  # 10秒超时
            
            try:
                # 尝试获取资金流向数据
                fund_flow = ak.stock_individual_fund_flow_rank(indicator="5日")
                
                if fund_flow.empty:
                    print("无法获取资金流向数据，使用默认值")
                    return self._get_default_fund_flow()
                
                # 查找股票
                stock_row = fund_flow[fund_flow['代码'] == symbol]
                if stock_row.empty:
                    return self._get_default_fund_flow()
                
                # 提取资金流向数据
                flow_data = stock_row.iloc[0]
                
                return {
                    'main_net_inflow': flow_data.get('主力净流入-净额', 0),
                    'retail_net_inflow': flow_data.get('散户净流入-净额', 0),
                    'super_large_net_inflow': flow_data.get('超大单净流入-净额', 0),
                    'large_net_inflow': flow_data.get('大单净流入-净额', 0),
                    'medium_net_inflow': flow_data.get('中单净流入-净额', 0),
                    'small_net_inflow': flow_data.get('小单净流入-净额', 0)
                }
                
            finally:
                socket.setdefaulttimeout(original_timeout)
            
        except Exception as e:
            print(f"获取资金流向数据失败: {e}")
            return self._get_default_fund_flow()
    
    def _get_default_fund_flow(self):
        """返回默认的资金流向数据"""
        return {
            'main_net_inflow': 0,
            'retail_net_inflow': 0,
            'super_large_net_inflow': 0,
            'large_net_inflow': 0,
            'medium_net_inflow': 0,
            'small_net_inflow': 0
        } 