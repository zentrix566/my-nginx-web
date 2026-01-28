import os
import datetime

# 1. 读取导航栏模板
with open('nav.html', 'r', encoding='utf-8') as f:
    nav_content = f.read()

# 2. 定义需要处理的文件列表
files_to_process = ['index.html', 'web/status.html', 'web/about.html', 'web/terminal.html']

# 获取金句数据（复用之前的逻辑）
# quote = fetch_quote() ... 这里省略之前的获取逻辑，保持你现有的不变

for file_path in files_to_process:
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 注入导航栏：寻找 并替换
    if '' in content:
        content = content.replace('', nav_content)
    
    # 注入金句和时间（仅针对 status.html）
    if 'status.html' in file_path:
        content = content.replace('{{BUILD_TIME}}', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # content = content.replace('{{QUOTE_PLACEHOLDER}}', quote)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Successfully injected navigation and data into all pages.")