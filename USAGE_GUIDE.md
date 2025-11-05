# 使用指南 | Usage Guide

## 🎯 使用步骤

### 第一步：获取 FRED API 密钥

1. 打开浏览器，访问：https://fred.stlouisfed.org/
2. 点击右上角 "Sign In" 或 "Create Account"
3. 登录后，访问：https://fred.stlouisfed.org/docs/api/api_key.html
4. 点击 "Request API Key" 按钮
5. 填写表格（填写用途可以写 "Academic Research" 或 "Personal Analysis"）
6. 提交后立即获得 32 位的 API 密钥，类似这样：
   ```
   a1b2c3d4e5f6789012345678901234
   ```

### 第二步：安装 Python 环境

确保你的电脑安装了 Python 3.7 或更高版本。

检查 Python 版本：
```bash
python --version
# 或
python3 --version
```

### 第三步：安装依赖包

在项目目录下运行：

```bash
pip install -r requirements.txt
```

或者使用 pip3：
```bash
pip3 install -r requirements.txt
```

### 第四步：运行脚本

使用你的 API 密钥运行脚本：

```bash
python fetch_shutdown_data_final.py YOUR_API_KEY
```

**实际示例：**
```bash
python fetch_shutdown_data_final.py a1b2c3d4e5f6789012345678901234
```

### 第五步：查看结果

脚本运行完成后，会在当前目录生成 `us_shutdown_financial_data.xlsx` 文件。

用 Excel、WPS 或者 LibreOffice 打开查看数据。

## 📊 输出示例

### 控制台输出示例

```
======================================================================
US Government Shutdown Financial Data Fetcher
美国政府停摆金融数据获取工具
======================================================================

✓ Using API key: a1b2c3d4e5...

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
Creating Excel file: us_shutdown_financial_data.xlsx
======================================================================
✓ Excel file created successfully!
  File: us_shutdown_financial_data.xlsx
  Sheets: 4

======================================================================
✓ SUCCESS! Data fetched and saved
======================================================================
```

### Excel 文件内容

#### Summary 表格

| No. | Period | Data Start | Data End | Total Records | Indicators |
|-----|--------|------------|----------|---------------|------------|
| 1 | 16天停摆 (2013年10月1日至10月17日) | 2012-10-01 | 2014-10-17 | 522 | TGA, EFFR, Reserves |
| 2 | 35天停摆 (2018年12月22日至2019年1月25日) | 2017-12-22 | 2020-01-25 | 789 | TGA, EFFR, SOFR, Reserves |
| 3 | 持续中 (2025年10月1日至今) | 2024-10-01 | 2025-11-05 | 312 | TGA, EFFR, SOFR, Reserves |

#### 数据表格示例 (1_2013)

| DATE | Treasury General Account | Effective Federal Funds Rate | Bank Reserves |
|------------|-----------------|---------|-----------|
| 2012-10-03 | 85,355 | 0.14 | 1,544,000 |
| 2012-10-10 | 32,583 | 0.15 | 1,486,000 |
| ... | ... | ... | ... |

> **注意**：停摆期间的数据行会用浅红色背景高亮显示

## 🔧 高级使用

### 环境变量方式

如果不想每次都输入 API 密钥，可以设置环境变量：

**Windows (CMD):**
```cmd
set FRED_API_KEY=your_api_key_here
python fetch_shutdown_data_final.py %FRED_API_KEY%
```

**Windows (PowerShell):**
```powershell
$env:FRED_API_KEY="your_api_key_here"
python fetch_shutdown_data_final.py $env:FRED_API_KEY
```

**Mac/Linux:**
```bash
export FRED_API_KEY="your_api_key_here"
python fetch_shutdown_data_final.py $FRED_API_KEY
```

### 修改日期范围

如果需要修改数据获取的时间范围，可以编辑 `fetch_shutdown_data_final.py` 文件中的 `SHUTDOWN_PERIODS` 配置：

```python
SHUTDOWN_PERIODS = [
    {
        'name': '2013 Government Shutdown',
        'shutdown_start': '2013-10-01',
        'shutdown_end': '2013-10-17',
        'data_start': '2012-10-01',  # 修改这里
        'data_end': '2014-10-17',     # 修改这里
        'description': '16天停摆 (2013年10月1日至10月17日)'
    },
    # ...
]
```

## 📊 数据分析建议

获取到数据后，可以进行以下分析：

1. **趋势分析**：观察停摆前后各指标的变化趋势
2. **波动性分析**：比较停摆期间和正常时期的数据波动
3. **相关性分析**：分析不同指标之间的关系
4. **对比分析**：比较不同停摆时期的数据特征

推荐使用工具：
- Excel / WPS 的数据透视表和图表功能
- Python: pandas, matplotlib, seaborn
- R: ggplot2, dplyr

## ❓ 常见问题

### Q1: 脚本运行很慢？
A: FRED API 有速率限制，脚本中已经添加了延迟（每个请求间隔0.2秒）。这是正常现象。

### Q2: 某些数据显示为空？
A: 正常情况，原因可能是：
- SOFR 从2018年4月才开始发布
- 某些日期是节假日，没有交易数据
- FRED 数据更新可能有延迟

### Q3: API 密钥失效？
A: 重新访问 https://fred.stlouisfed.org/docs/api/api_key.html 生成新的密钥

### Q4: 可以每天自动运行吗？
A: 可以！设置定时任务（Windows Task Scheduler / Linux Cron Job）自动运行脚本

## 📧 技术支持

遇到问题？
1. 检查 README.md 中的故障排除部分
2. 验证 API 密钥是否有效
3. 确保网络连接正常
4. 提交 Issue 寻求帮助

---

**祝数据分析顺利！** 📈
