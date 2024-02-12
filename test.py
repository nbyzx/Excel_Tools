# 用来测试代码用的
import random
from datetime import datetime, timedelta


# 生成随机的身份证号码
def generate_id_number():
    id_number = ''
    for _ in range(17):
        id_number += str(random.randint(0, 9))
    id_number += random.choice(['1', '3', '5', '7', '9'])
    return id_number


# 生成随机的年月日
def generate_date():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2000, 12, 31)

    random_days = random.randint(1, (end_date - start_date).days)
    date = start_date + timedelta(days=random_days)
    return date.strftime('%Y-%m-%d')


# 生成随机的年份
def generate_year():
    return str(random.randint(1950, 2000))


# 生成20条身份证号码+年月日+年份的组合
for _ in range(20):
    id_number = generate_id_number()
    date = generate_date()
    year = generate_year()
    print(f'身份证号码：{id_number}，日期：{date}，年份：{year}')

