# 美国政府停摆金融数据分析工具

US Government Shutdown Financial Data Analysis Tool

## 📊 项目简介

本工具用于获取和分析美国政府停摆期间的关键金融指标数据，包括：

- **TGA** (Treasury General Account): 美国财政部一般账户余额
- **EFFR** (Effective Federal Funds Rate): 有效联邦基金利率
- **SOFR** (Secured Overnight Financing Rate): 担保隔夜融资利率
- **Bank Reserves**: 银行准备金

## 🎯 涵盖的停摆时期

1. **2013年政府停摆** (16天)
   - 停摆时间：2013-10-01 至 2013-10-17
   - 数据范围：2012-10-01 至 2014-10-17

2. **2018-2019年政府停摆** (35天)
   - 停摆时间：2018-12-22 至 2019-01-25
   - 数据范围：2017-12-22 至 2020-01-25

3. **2025年政府停摆** (持续中)
   - 停摆时间：2025-10-01 至今
   - 数据范围：2024-10-01 至最新

每个时期的数据包含停摆前一年和停摆后一年的数据，用于对比分析。

## 🚀 快速开始

### 1. 获取 FRED API 密钥 (免费)

1. 访问 [FRED API 注册页面](https://fred.stlouisfed.org/docs/api/api_key.html)
2. 点击 "Request API Key"
3. 登录或创建账户
4. 填写简单的申请表单
5. 立即获得免费的 API 密钥

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行脚本

```bash
python fetch_shutdown_data_final.py YOUR_API_KEY_HERE
```

将 `YOUR_API_KEY_HERE` 替换为你的实际 API 密钥。

### 示例

```bash
python fetch_shutdown_data_final.py abcdef1234567890abcdef1234567890
```

## 📁 输出文件

脚本会生成一个 Excel 文件：`us_shutdown_financial_data.xlsx`

### Excel 文件结构

- **Summary**: 数据汇总表
- **1_2013**: 2013年停摆数据
- **2_2018-2019**: 2018-2019年停摆数据
- **3_2025**: 2025年停摆数据

每个数据表包含：
- 日期索引
- TGA (财政部一般账户)
- EFFR (有效联邦基金利率)
- SOFR (担保隔夜融资利率)
- Bank Reserves (银行准备金)

停摆期间的数据行会用浅红色高亮显示。

## 📈 数据来源

所有数据来自 [FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/)，由圣路易斯联邦储备银行维护。

### 数据链接

- TGA: https://fred.stlouisfed.org/series/WTREGEN
- EFFR: https://fred.stlouisfed.org/series/EFFR
- SOFR: https://fred.stlouisfed.org/series/SOFR
- Bank Reserves: https://fred.stlouisfed.org/series/WRESBAL

## 🛠️ 技术栈

- Python 3.7+
- pandas: 数据处理
- requests: API 请求
- openpyxl: Excel 文件生成和格式化

## 📋 依赖清单

查看 `requirements.txt`:
```
pandas>=2.0.0
requests>=2.31.0
openpyxl>=3.1.0
```

## ⚠️ 注意事项

1. **SOFR 数据**: SOFR 是从2018年4月开始发布的，所以2013年的数据中不会包含 SOFR。
2. **数据频率**: 不同指标的发布频率可能不同（每日、每周等）。
3. **API 限制**: FRED API 有使用限制，正常使用不会超过限制。
4. **网络连接**: 需要稳定的网络连接来访问 FRED API。

## 🔍 故障排除

### 问题: 403 Forbidden 错误
**解决方案**: 确保使用的是有效的 FRED API 密钥。

### 问题: No data fetched
**解决方案**:
1. 检查网络连接
2. 验证 API 密钥是否有效
3. 确认 FRED API 服务是否正常

### 问题: 某些指标缺失数据
**解决方案**: 这是正常的，某些指标在特定时期可能没有数据（如 SOFR 在2018年之前）。

## 📧 联系方式

如有问题或建议，请提交 Issue。

## 📄 许可证

MIT License

## 🙏 致谢

- 数据提供：Federal Reserve Bank of St. Louis (FRED)
- 开源社区的各种优秀工具和库

---

**最后更新**: 2025-11-05
