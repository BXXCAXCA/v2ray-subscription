import requests
import re
import os
from datetime import datetime

def scrape_v2ray_subscription(url):
    """爬取V2ray订阅地址"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        
        drive_links = re.findall(r'https://drive\.google\.com/uc\?export=download&id=[^\s<>"]+', response.text)
        
        for link in drive_links:
            link_pos = response.text.find(link)
            context = response.text[max(0, link_pos-200):link_pos]
            
            if 'v2ray' in context.lower() or 'karing' in context.lower() or 'quantumult' in context.lower():
                return link
        
        return None
        
    except Exception as e:
        print(f"爬取失败: {e}")
        return None

def download_config(subscription_url, output_file):
    """下载订阅配置文件"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(subscription_url, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"配置文件已保存到: {output_file}")
            return True
        else:
            print(f"下载失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"下载失败: {e}")
        return False

if __name__ == "__main__":
    source_url = os.getenv('SOURCE_URL')
    
    if not source_url:
        print("错误: 未设置 SOURCE_URL 环境变量")
        exit(1)
    
    print("正在爬取订阅地址...")
    subscription_url = scrape_v2ray_subscription(source_url)
    
    if subscription_url:
        print(f"找到订阅地址: {subscription_url}")
        
        # 保存订阅地址
        with open('subscription_url.txt', 'w') as f:
            f.write(subscription_url)
        
        # 下载配置文件
        print("正在下载配置文件...")
        if download_config(subscription_url, 'docs/v2ray_config.txt'):
            # 更新时间戳
            with open('docs/last_update.txt', 'w') as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'))
            print("更新成功！")
        else:
            print("下载配置文件失败")
    else:
        print("未找到订阅地址")
