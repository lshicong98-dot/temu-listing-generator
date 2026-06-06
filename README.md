# Temu AI Listing Generator

一个帮助Temu卖家自动生成优化的英文商品标题和描述的工具。基于DeepSeek API实现AI自动生成，支持单个生成和批量处理。

## 功能特点

- 🎯 **AI智能生成**：基于DeepSeek大语言模型生成高质量listing
- 🌐 **英文输出**：生成符合Temu/Amazon跨境平台要求的英文listing
- 📝 **SEO优化**：标题和描述符合SEO规范，包含关键词
- 📦 **批量处理**：支持CSV文件批量上传，批量生成并打包下载
- 🖥️ **Web界面**：简洁美观的Web界面，支持中文操作

## 生成内容

1. **Product Title**：优化的商品标题（60-80字符）
2. **Bullet Points**：5个核心卖点列表
3. **Description**：详细产品描述（150-200词）

## 技术栈

- Python 3.x
- Flask 3.x
- DeepSeek API
- HTML/CSS/JavaScript

## 安装与运行

### 1. 安装依赖

```bash
pip install flask requests python-dotenv
```

### 2. 设置API Key

方式一：设置环境变量
```bash
# Linux/Mac
export DEEPSEEK_API_KEY="your-api-key"

# Windows PowerShell
$env:DEEPSEEK_API_KEY="your-api-key"
```

方式二：在Web界面中输入

### 3. 启动服务

```bash
python app.py
```

访问 http://localhost:5000 即可使用

## 使用方法

### 单个生成

1. 在"单个生成"标签页输入商品信息
2. 点击"生成英文Listing"按钮
3. 复制生成的标题、卖点和描述

### 批量处理

1. 创建CSV文件，格式如下：
```csv
product_name,selling_points,target_market
Wireless Earbuds,Noise Cancelling,30H Battery,USA
USB Cable,Fast Charging,Durable,Global
```

2. 在"批量处理"标签页上传CSV文件
3. 点击"批量生成并下载"按钮
4. 获取包含所有listing的ZIP文件

## CSV文件格式

| 列名 | 说明 | 必填 |
|------|------|------|
| product_name | 商品名称 | ✅ |
| selling_points | 核心卖点（逗号分隔） | ❌ |
| target_market | 目标市场 | ❌ |

## 获取DeepSeek API Key

1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册账号
3. 获取免费API Key

## 项目结构

```
temu-listing-generator/
├── app.py                 # Flask应用主文件
├── listing_generator.py   # Listing生成器核心代码
├── templates/
│   └── index.html         # Web界面模板
├── sample_products.csv    # 示例CSV文件
├── .gitignore            # Git忽略配置
└── README.md             # 项目说明文档
```

## 注意事项

- 请勿将API Key提交到版本控制
- 免费API有调用次数限制，请合理使用
- 生成的listing建议人工审核后再发布

## License

MIT License