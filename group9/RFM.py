import sqlite3
dbfile = "db.db"
conn = sqlite3.connect(dbfile)
rows = conn.execute("SELECT * FROM `order`;")
data = [list(row) for row in rows]

conn.close()

from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt


# Recency
today = datetime.now()

# 儲存每個客戶最近購買日
customer_last_purchase = defaultdict(lambda: datetime.min)

# 找出最近購買日最大值
for item in data:
    customer = item[0]  # 客戶名字
    date_string = item[4]  # 找日期
    date = datetime.strptime(date_string, '%Y-%m-%d')  # 將日期轉為 datetime
    if date > customer_last_purchase[customer]:  # 找出最近購買日最大值
        customer_last_purchase[customer] = date

# 計算每個客戶 Recency
for item in data:
    customer = item[0]  
    date_string = item[4] 
    date = datetime.strptime(date_string, '%Y-%m-%d')  # 將日期轉為 datetime
    recency = (today - customer_last_purchase[customer]).days  # 用客戶最近購買日計算 Recency
    item.append(recency)  

# 儲存RFM
customer_info = defaultdict(lambda: {'frequency': 0, 'monetary': 0, 'recency': 0})

# 計算RFM
for item in data:
    customer = item[0]  # 客戶名字
    amount = item[1]  # 購買金額
    recency = item[5]  # recency
    if amount is not None:  # 如果金額不為0，家上購買金額
        customer_info[customer]['monetary'] += amount
    customer_info[customer]['frequency'] += 1  # 增加購買頻率
    if recency > customer_info[customer]['recency']:  # 更新最近交易日期（取最大值）
        customer_info[customer]['recency'] = recency


# 提取每個顧客RFM值
customers = list(customer_info.keys())
frequency = [info['frequency'] for info in customer_info.values()]
monetary = [info['monetary'] for info in customer_info.values()]
recency = [info['recency'] for info in customer_info.values()]

# 畫圖
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Recency vs Frequency
axs[0].scatter(recency, frequency, c='blue', alpha=0.8, edgecolors='w', s=100)
axs[0].set_xlabel('Recency')
axs[0].set_ylabel('Frequency')
axs[0].set_title('Recency vs Frequency')
axs[0].grid(True)

# Frequency vs Monetary
axs[1].scatter(frequency, monetary, c='red', alpha=0.8, edgecolors='w', s=100)
axs[1].set_xlabel('Frequency')
axs[1].set_ylabel('Monetary')
axs[1].set_title('Frequency vs Monetary')
axs[1].grid(True)

# Recency vs Monetary
axs[2].scatter(recency, monetary, c='green', alpha=0.8, edgecolors='w', s=100)
axs[2].set_xlabel('Recency')
axs[2].set_ylabel('Monetary')
axs[2].set_title('Recency vs Monetary')
axs[2].grid(True)

# 調整間距
plt.tight_layout()
plt.show()