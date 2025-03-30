# GitHub 热门项目爬虫

这是一个用于抓取 GitHub Trending 页面数据的 Python 爬虫项目。它能够自动获取每日、每周和每月的 GitHub 热门仓库信息，并将数据保存为 JSON 格式。

## 功能特点

- 支持抓取每日、每周、每月的热门仓库数据
- 自动重试机制，提高数据获取的稳定性
- 完整的错误处理和日志记录
- 数据以JSON格式保存，便于后续分析和处理
- 支持获取仓库的详细信息：
  - 仓库名称和链接
  - 项目描述
  - 编程语言
  - 总星标数
  - 当日新增星标数

## 使用方法

1. 确保已安装所需的Python库：
```bash
pip install requests beautifulsoup4
```

2. 运行脚本：
```bash
python github_hot.py
```

3. 数据将保存在项目目录下的 `data` 文件夹中，文件名格式为：
   `github_trending_[时间范围]_[时间戳].json`

## 数据格式

输出的JSON文件包含以下字段：
```json
{
    "timestamp": "抓取时间",
    "time_range": "时间范围（daily/weekly/monthly）",
    "count": "仓库数量",
    "repositories": [
        {
            "name": "仓库名称",
            "url": "仓库URL",
            "description": "项目描述",
            "language": "编程语言",
            "stars": "总星标数",
            "stars_today": "今日新增星标数"
        }
    ]
}
```

## 注意事项

- 请遵守 GitHub 的使用规范和访问频率限制
- 建议适当设置抓取间隔，避免频繁请求
- 确保网络连接稳定

## 许可证

MIT License
