# spider-practice
爬虫练习
# 爬虫练习

## 在线预览

[点击访问](https://dengxinyan2026.github.io/spider-practice/)

## 项目结构
spider-practice/
├── index.html          # 练习靶场页面
├── spider_practice.py  # Python 爬虫代码
└── README.md           # 项目说明

## 练习模块

| 练习  | 内容        | XPath 技巧 |
|  1   | 基础表格     | `//table/thead/tr/th` |
|  2   | 多层嵌套     | `//ul[@class="game-list"]/li` |
|  3   | 不规则表格   | `//table/tr[1]/td` |
|  4   | CSS 类选择器 | `//div[@class="movie-card"]` |
|  5   | 隐藏数据     | 提取 `display:none` 内容 |


### 1. 查看页面
直接打开 `index.html` 或访问在线预览

### 2. 运行爬虫
```bash
pip install lxml
python spider_practice.py
