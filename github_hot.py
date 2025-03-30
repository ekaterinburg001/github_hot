import requests
import json
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 创建保存数据的目录
def create_data_directory():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logging.info(f"创建数据目录: {data_dir}")
    return data_dir

# 获取GitHub Trending页面内容
def fetch_github_trending(time_range='daily', language=''):
    url = f"https://github.com/trending/{language}?since={time_range}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"请求失败 (尝试 {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                logging.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                logging.error("达到最大重试次数，无法获取数据")
                raise

# 解析GitHub Trending页面
def parse_trending_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    trending_repos = []
    
    # 查找所有仓库项目
    repo_list = soup.select('article.Box-row')
    
    for repo in repo_list:
        try:
            # 获取仓库名称和链接
            repo_name_element = repo.select_one('h2.h3 a')
            if not repo_name_element:
                continue
                
            full_name = repo_name_element.get_text(strip=True)
            repo_url = f"https://github.com{repo_name_element['href']}"
            
            # 获取仓库描述
            description_element = repo.select_one('p')
            description = description_element.get_text(strip=True) if description_element else ""
            
            # 获取编程语言
            language_element = repo.select_one('span[itemprop="programmingLanguage"]')
            language = language_element.get_text(strip=True) if language_element else "Unknown"
            
            # 获取星标数
            stars_element = repo.select('a.Link--muted')[0]
            stars_text = stars_element.get_text(strip=True)
            stars = stars_text.replace(',', '')
            
            # 获取今日新增星标数
            try:
                today_stars_element = repo.select_one('span.d-inline-block.float-sm-right')
                today_stars = today_stars_element.get_text(strip=True).replace('stars today', '').strip() if today_stars_element else "0"
            except:
                today_stars = "0"
            
            # 添加到结果列表
            trending_repos.append({
                'name': full_name,
                'url': repo_url,
                'description': description,
                'language': language,
                'stars': stars,
                'stars_today': today_stars
            })
            
        except Exception as e:
            logging.error(f"解析仓库时出错: {e}")
    
    return trending_repos

# 保存数据到JSON文件
def save_to_json(data, data_dir, time_range='daily'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"github_trending_{time_range}_{timestamp}.json"
    file_path = os.path.join(data_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logging.info(f"数据已保存到: {file_path}")
    return file_path

# 主函数
def main():
    try:
        # 创建数据目录
        data_dir = create_data_directory()
        
        # 定义要爬取的时间范围
        time_ranges = ['daily', 'weekly', 'monthly']
        
        for time_range in time_ranges:
            logging.info(f"正在爬取 {time_range} 热门仓库...")
            
            # 获取并解析页面
            html_content = fetch_github_trending(time_range)
            trending_repos = parse_trending_page(html_content)
            
            if trending_repos:
                # 添加元数据
                result = {
                    'timestamp': datetime.now().isoformat(),
                    'time_range': time_range,
                    'count': len(trending_repos),
                    'repositories': trending_repos
                }
                
                # 保存数据
                save_to_json(result, data_dir, time_range)
            else:
                logging.warning(f"未找到 {time_range} 热门仓库")
        
        logging.info("所有数据爬取完成")
        
    except Exception as e:
        logging.error(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()