import sqlite3
dbfile = "db.db"
conn = sqlite3.connect(dbfile)
rows = conn.execute("SELECT * FROM `order`;")
data = [list(row) for row in rows]

conn.close()

import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

start_date = datetime(2023, 11, 20)
end_date = datetime(2023, 12, 30)  
num_days = (end_date - start_date).days + 1

dates = [start_date + timedelta(days=i) for i in range(num_days)]
daily_sales = {date: 0 for date in dates}

for item in data:
    date_str = item[4]
    sale_amount = item[1]
    sale_date = datetime.strptime(date_str, '%Y-%m-%d')
    daily_sales[sale_date] += sale_amount

# 將銷售數據轉換為列表
dates = list(daily_sales.keys())
sales = list(daily_sales.values())

#畫圖
plt.figure(figsize=(10, 6))

# 銷售線
plt.plot(dates, sales, marker='o', linestyle='-', label='sales')

# 填充銷售線下方顏色
plt.fill_between(dates, sales, color='#3887BE', alpha=0.3)

plt.title('Daily sales')
plt.xlabel('Date')
plt.ylabel('Sales(Dollars)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# 顯示圖表
plt.show()