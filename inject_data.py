import requests
import datetime

def main():
    # 获取数据
    try:
        res = requests.get("https://v1.hitokoto.cn/?c=i")
        quote = res.json()['hitokoto']
    except:
        quote = "保持好奇心，继续实验。"

    build_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 重点：这里改为操作 status.html
    with open('status.html', 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('{{QUOTE_PLACEHOLDER}}', quote)
    content = content.replace('{{BUILD_TIME}}', build_time)

    with open('status.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    main()