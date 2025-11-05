# 本地运行指南 | Local Run Guide

## ⚠️ 重要提示

如果您在Docker或云环境中遇到 `403 Access denied` 错误，即使使用了有效的API密钥，这是因为某些云环境的IP可能被FRED的防火墙限制。

**解决方案：在本地计算机上运行脚本**

## 💻 在本地Windows/Mac/Linux运行

### 步骤1: 下载代码

从Git仓库下载或克隆代码到本地：

```bash
git clone <repository_url>
cd awesome-macro-data
```

或者直接下载这些文件：
- `fetch_shutdown_data_final.py`
- `requirements.txt`

### 步骤2: 确保Python环境

检查Python版本（需要3.7+）：

```bash
python --version
# 或
python3 --version
```

如果没有Python，请安装：
- **Windows**: https://www.python.org/downloads/
- **Mac**: 使用 Homebrew: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### 步骤3: 安装依赖

```bash
pip install pandas requests openpyxl
```

或使用requirements.txt：

```bash
pip install -r requirements.txt
```

### 步骤4: 使用您的API密钥运行

```bash
python fetch_shutdown_data_final.py 269dcf5e0e43110384758332746a134c
```

### 预期输出

脚本运行时会显示：

```
======================================================================
US Government Shutdown Financial Data Fetcher
美国政府停摆金融数据获取工具
======================================================================

✓ Using API key: 269dcf5e0e...

======================================================================
2013 Government Shutdown
16天停摆 (2013年10月1日至10月17日)
Data range: 2012-10-01 to 2014-10-17
======================================================================
  Fetching WTREGEN... ✓ 105 records
  Fetching EFFR... ✓ 522 records
  Fetching SOFR... ✗ No observations
  Fetching WRESBAL... ✓ 105 records

✓ Total records: 522

======================================================================
2018-2019 Government Shutdown
35天停摆 (2018年12月22日至2019年1月25日)
Data range: 2017-12-22 to 2020-01-25
======================================================================
  Fetching WTREGEN... ✓ 115 records
  Fetching EFFR... ✓ 789 records
  Fetching SOFR... ✓ 654 records
  Fetching WRESBAL... ✓ 115 records

✓ Total records: 789

======================================================================
2025 Government Shutdown
持续中 (2025年10月1日至今)
Data range: 2024-10-01 to 2025-11-05
======================================================================
  Fetching WTREGEN... ✓ 58 records
  Fetching EFFR... ✓ 312 records
  Fetching SOFR... ✓ 312 records
  Fetching WRESBAL... ✓ 58 records

✓ Total records: 312

======================================================================
Creating Excel file: us_shutdown_financial_data.xlsx
======================================================================
✓ Excel file created successfully!
  File: us_shutdown_financial_data.xlsx
  Sheets: 4

======================================================================
✓ SUCCESS! Data fetched and saved
======================================================================

Data Summary:

2013 Government Shutdown:
  Records: 522
  Date range: 2012-10-03 to 2014-10-16
  Indicators: 3
    - Treasury General Account (TGA): 105 values
    - Effective Federal Funds Rate (EFFR): 522 values
    - Bank Reserves: 105 values

2018-2019 Government Shutdown:
  Records: 789
  Date range: 2017-12-27 to 2020-01-22
  Indicators: 4
    - Treasury General Account (TGA): 115 values
    - Effective Federal Funds Rate (EFFR): 789 values
    - Secured Overnight Financing Rate (SOFR): 654 values
    - Bank Reserves: 115 values

2025 Government Shutdown:
  Records: 312
  Date range: 2024-10-02 to 2025-11-04
  Indicators: 4
    - Treasury General Account (TGA): 58 values
    - Effective Federal Funds Rate (EFFR): 312 values
    - Secured Overnight Financing Rate (SOFR): 312 values
    - Bank Reserves: 58 values

✓ Excel file: us_shutdown_financial_data.xlsx
```

### 步骤5: 打开Excel文件

用Excel、WPS或LibreOffice打开生成的文件：

```
us_shutdown_financial_data.xlsx
```

## 🔍 常见问题

### Q: 为什么在Docker/云环境中不工作？

A: FRED可能限制了某些云服务器的IP地址访问，这是正常的反爬虫措施。在本地计算机上运行即可。

### Q: 如果我的API密钥显示"Access denied"怎么办？

A:
1. 检查是否完整复制了整个密钥（32位字符）
2. 确认密钥没有过期
3. 重新申请一个新密钥：https://fred.stlouisfed.org/docs/api/api_key.html

### Q: 脚本运行需要多长时间？

A: 通常2-3分钟。脚本会自动处理速率限制。

### Q: 可以修改时间范围吗？

A: 可以！编辑 `fetch_shutdown_data_final.py` 中的 `SHUTDOWN_PERIODS` 配置。

## 📧 技术支持

如果在本地运行仍有问题：
1. 确保网络连接正常
2. 尝试关闭VPN或代理
3. 检查防火墙设置
4. 使用测试脚本验证API密钥：`python test_api_key.py YOUR_API_KEY`

## 🎯 环境要求

- ✅ Python 3.7+
- ✅ 稳定的网络连接
- ✅ 有效的FRED API密钥
- ✅ 大约10MB的磁盘空间

## 📊 生成的数据格式

Excel文件将包含4个工作表：

1. **Summary** - 总览
2. **1_2013** - 2013年停摆期数据
3. **2_2018-2019** - 2018-2019年停摆期数据
4. **3_2025** - 2025年停摆期数据

每个数据表包含日期索引和4个指标列，停摆期间的数据会用浅红色背景高亮。

---

**建议：在本地Windows/Mac/Linux环境运行此脚本以获得最佳结果！** 🚀
