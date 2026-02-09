import datetime

# 获取当前时间，格式化为 'YYYY-MM-DD HH:MM:SS'
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 打开 quotes.txt 文件并逐行读取
with open('quotes.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 生成 SQL 语句
for line in lines:
    content = line.strip().replace("'", "''")  # 转义单引号，防止 SQL 注入或语法错误
    if not content:  # 跳过空行
        continue
    sql = f"INSERT INTO \"public\".\"quotes\" (\"content\", \"author\", \"created_at\") VALUES ('{content}', '佚名', '{current_time}');"
    print(sql)