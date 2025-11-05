# 快速开始 | Quick Start

## 最简单的 3 步使用方法

### 1️⃣ 获取免费 API 密钥（1分钟）

访问：https://fred.stlouisfed.org/docs/api/api_key.html

点击 "Request API Key" → 登录/注册 → 立即获得密钥

### 2️⃣ 安装依赖（30秒）

```bash
pip install pandas requests openpyxl
```

### 3️⃣ 运行脚本（2-3分钟）

```bash
python fetch_shutdown_data_final.py YOUR_API_KEY
```

**完成！** 会生成 `us_shutdown_financial_data.xlsx` 文件 📊

---

## 一行命令完成所有操作

```bash
pip install pandas requests openpyxl && python fetch_shutdown_data_final.py YOUR_API_KEY
```

---

## 获取的数据

✅ **TGA** - 美国财政部一般账户
✅ **EFFR** - 有效联邦基金利率
✅ **SOFR** - 担保隔夜融资利率
✅ **Bank Reserves** - 银行准备金

✅ **三个停摆时期**：2013年 / 2018-2019年 / 2025年
✅ **时间跨度**：每个时期停摆前后各一年的数据

---

## 输出文件

📁 `us_shutdown_financial_data.xlsx`

包含 4 个工作表：
- **Summary**: 数据概览
- **1_2013**: 2013年停摆数据
- **2_2018-2019**: 2018-2019年停摆数据
- **3_2025**: 2025年停摆数据

停摆期间的数据会用 **浅红色高亮** 显示！

---

## 需要帮助？

📖 详细文档：[README.md](README.md)
📚 使用指南：[USAGE_GUIDE.md](USAGE_GUIDE.md)

---

**就这么简单！** 🎉
