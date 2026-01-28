import os
import datetime

# 定义要处理的文件（现在只处理 status.html）
target_file = 'web/status.html'

if os.path.exists(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换构建时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = content.replace('{{BUILD_TIME}}', current_time)

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully updated build time in {target_file}")
else:
    print(f"Error: {target_file} not found!")