import os
import datetime

# 1. 读取导航栏模板
if os.path.exists('nav.html'):
    with open('nav.html', 'r', encoding='utf-8') as f:
        nav_content = f.read()
else:
    print("Error: nav.html not found!")
    nav_content = ""

# 2. 定义需要处理的文件列表
files_to_process = ['index.html', 'web/status.html', 'web/about.html', 'web/terminal.html']

# 占位符定义（必须与 HTML 中的注释完全一致）
NAV_TAG = ''

for file_path in files_to_process:
    if not os.path.exists(file_path):
        print(f"Skipping: {file_path} (File not found)")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 核心步骤：将 替换为 nav.html 的内容
    if NAV_TAG in content:
        content = content.replace(NAV_TAG, nav_content)
        print(f"Injected navigation into {file_path}")
    
    # 注入时间（仅针对 status.html）
    if 'status.html' in file_path:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = content.replace('{{BUILD_TIME}}', current_time)
        print(f"Injected build time into {file_path}")

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("All tasks completed successfully.")