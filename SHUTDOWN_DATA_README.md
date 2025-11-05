# 美国政府停摆金融数据获取工具

## 📋 概述

本工具用于获取三次美国政府停摆期间的关键金融数据，包括：

### 停摆时间范围
1. **2013年停摆**: 2013-10-01 至 2013-10-17
2. **2018-2019年停摆**: 2018-12-22 至 2019-01-25
3. **2025年停摆**: 2025-10-01 至今（持续中）

### 数据指标
- **TGA** (Treasury General Account): seriesID=WTREGEN
- **EFFR** (Effective Federal Funds Rate): seriesID=EFFR
- **SOFR** (Secured Overnight Financing Rate): seriesID=SOFR
- **银行准备金** (Bank Reserves): seriesID=WRESBAL

### 数据范围
每次停摆前一年开始到停摆结束后一年的数据（2025年停摆获取到最新数据）

---

## ⚠️ 重要提示：API Key 已失效

您提供的API key已经失效或过期。需要获取新的FRED API key才能使用本工具。

---

## 🔑 如何获取FRED API Key

### 步骤 1: 注册/登录 FRED 账户
访问 [FRED官网](https://fred.stlouisfed.org/) 并点击右上角的 "Sign In" 或 "Create Account"

### 步骤 2: 申请API Key
1. 登录后，访问 [API Keys 页面](https://fredaccount.stlouisfed.org/apikeys)
2. 点击 "Request API Key" 按钮
3. 填写简单的申请表单：
   - API Key Name: 填写任意名称（如 "Shutdown Data Analysis"）
   - Purpose: 选择 "Education" 或 "Research"
   - Description: 简单描述用途
4. 提交后通常立即获得批准
5. 复制您的32位API Key

### 步骤 3: 使用API Key
获得API key后，直接在命令行中使用即可，无需额外配置文件。

---

## 🚀 使用方法

### 1. 测试API Key（推荐）
```bash
python3 test_api_key.py YOUR_API_KEY
```

如果看到 "✓ Your API key is working perfectly!"，说明API key有效。

### 2. 运行数据获取脚本
```bash
python3 fetch_shutdown_data_final.py YOUR_API_KEY
```

脚本将自动：
- 从FRED API获取三次停摆期间的所有指标数据
- 生成一个包含所有数据的Excel文件
- 在Excel文件中创建多个工作表（摘要+每个停摆期一个）
- 对停摆期间的数据进行高亮显示

### 3. 输出文件
- `us_shutdown_financial_data.xlsx` - 包含所有三次停摆的完整数据

---

## 📊 Excel文件结构

Excel文件 `us_shutdown_financial_data.xlsx` 包含：
- **Summary工作表**: 所有停摆期的汇总信息
- **1_2013工作表**: 2013年停摆期数据（包含所有四个指标）
- **2_2018-2019工作表**: 2018-2019年停摆期数据
- **3_2025工作表**: 2025年停摆期数据

每个数据工作表包含：
- **日期列**: 观测日期（已设置为索引）
- **TGA列**: Treasury General Account数据
- **EFFR列**: Effective Federal Funds Rate数据
- **SOFR列**: Secured Overnight Financing Rate数据
- **银行准备金列**: Bank Reserves数据

特色功能：
- 停摆期间的数据行会用浅红色高亮显示
- 表头使用深蓝色背景和白色字体
- 自动调整列宽
- 冻结首行便于滚动查看

---

## 📦 依赖包

脚本需要以下Python包（已自动安装）：
```bash
pip install pandas openpyxl requests
```

---

## 🔧 技术细节

### API 请求格式
```
https://api.stlouisfed.org/fred/series/observations?
  series_id=SERIESID&
  api_key=YOUR_API_KEY&
  file_type=csv&
  observation_start=YYYY-MM-DD&
  observation_end=YYYY-MM-DD
```

### 数据日期范围详情

| 停摆期 | 停摆开始 | 停摆结束 | 数据开始 | 数据结束 |
|--------|----------|----------|----------|----------|
| 2013 | 2013-10-01 | 2013-10-17 | 2012-10-01 | 2014-10-17 |
| 2018-2019 | 2018-12-22 | 2019-01-25 | 2017-12-22 | 2020-01-25 |
| 2025 | 2025-10-01 | 持续中 | 2024-10-01 | 2025-11-05 |

---

## ❓ 常见问题

### Q: API返回403错误怎么办？
A: 说明API key无效或过期，需要按照上述步骤获取新的API key。

### Q: 某个指标没有数据怎么办？
A: 有些指标可能在特定时间段没有数据（如SOFR在2018年4月才开始发布）。脚本会跳过这些指标并在Excel中不创建对应工作表。

### Q: 可以修改数据范围吗？
A: 可以！编辑 `fetch_shutdown_data.py` 中的 `SHUTDOWNS` 列表，修改 `data_start` 和 `data_end` 字段。

---

## 📝 文件清单

- `fetch_shutdown_data_final.py` - 主数据获取脚本（带格式化Excel输出）
- `test_api_key.py` - API key测试工具
- `SHUTDOWN_DATA_README.md` - 本说明文档

---

## 📞 获取帮助

- FRED API 文档: https://fred.stlouisfed.org/docs/api/
- API Key 申请: https://fredaccount.stlouisfed.org/apikeys
- FRED 支持: https://fred.stlouisfed.org/contactus/

---

**准备好了吗？**

1. ✅ 获取新的FRED API key
2. ✅ 测试API key: `python3 test_api_key.py YOUR_API_KEY`
3. ✅ 运行脚本: `python3 fetch_shutdown_data_final.py YOUR_API_KEY`
4. ✅ 查看生成的Excel文件: `us_shutdown_financial_data.xlsx`

祝数据分析顺利！📊
