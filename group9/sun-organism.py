from flask import Flask, render_template
from io import BytesIO
import base64
import sqlite3
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/RFM')
def RFM():
    # 连接数据库
    dbfile = "db.db"
    conn = sqlite3.connect(dbfile)
    rows = conn.execute("SELECT * FROM `order`;")
    data = [list(row) for row in rows]
    conn.close()

    # 处理数据

    # Recency
    today = datetime.now()
    customer_last_purchase = defaultdict(lambda: datetime.min)

    for item in data:
        customer = item[0]
        date_string = item[4]
        date = datetime.strptime(date_string, '%Y-%m-%d')
        if date > customer_last_purchase[customer]:
            customer_last_purchase[customer] = date

    for item in data:
        customer = item[0]
        date_string = item[4]
        date = datetime.strptime(date_string, '%Y-%m-%d')
        recency = (today - customer_last_purchase[customer]).days
        item.append(recency)

    # RFM 计算
    customer_info = defaultdict(lambda: {'frequency': 0, 'monetary': 0, 'recency': 0})

    for item in data:
        customer = item[0]
        amount = item[1]
        recency = item[5]
        if amount is not None:
            customer_info[customer]['monetary'] += amount
        customer_info[customer]['frequency'] += 1
        if recency > customer_info[customer]['recency']:
            customer_info[customer]['recency'] = recency

    customers = list(customer_info.keys())
    frequency = [info['frequency'] for info in customer_info.values()]
    monetary = [info['monetary'] for info in customer_info.values()]
    recency = [info['recency'] for info in customer_info.values()]

    # Matplotlib 图形绘制
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    axs[0].scatter(recency, frequency, c='blue', alpha=0.8, edgecolors='w', s=100)
    axs[0].set_xlabel('Recency')
    axs[0].set_ylabel('Frequency')
    axs[0].set_title('Recency vs Frequency')
    axs[0].grid(True)

    axs[1].scatter(frequency, monetary, c='red', alpha=0.8, edgecolors='w', s=100)
    axs[1].set_xlabel('Frequency')
    axs[1].set_ylabel('Monetary')
    axs[1].set_title('Frequency vs Monetary')
    axs[1].grid(True)

    axs[2].scatter(recency, monetary, c='green', alpha=0.8, edgecolors='w', s=100)
    axs[2].set_xlabel('Recency')
    axs[2].set_ylabel('Monetary')
    axs[2].set_title('Recency vs Monetary')
    axs[2].grid(True)

    # 将 Matplotlib 图形转换为 base64 编码的字符串
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # 关闭 Matplotlib 图形
    plt.close()

    return render_template('RFM.html', plot_url=plot_url)

@app.route('/orders')
def show_orders():
    # 在此模擬一些訂單資料
    orders_data = [
        {'customer_name': '客戶1', 'order_details': '訂單1 內容', 'order_status': '已完成', 'payment_status': '已付款'},
        {'customer_name': '客戶2', 'order_details': '訂單2 內容', 'order_status': '處理中', 'payment_status': '待付款'},
        {'customer_name': '客戶3', 'order_details': '訂單3 內容', 'order_status': '已取消', 'payment_status': '未付款'},
        # 加入更多訂單資料...
    ]

    return render_template('orders.html', orders=orders_data)

@app.route('/inventory')
def show_inventory():
    # 模擬一些庫存資料
    inventory_data = [
        {'product_name': '商品1', 'product_id': '001', 'stock_quantity': 50},
        {'product_name': '商品2', 'product_id': '002', 'stock_quantity': 75},
        {'product_name': '商品3', 'product_id': '003', 'stock_quantity': 30},
        # 加入更多庫存資料...
    ]

    return render_template('inventory.html', inventory=inventory_data)

@app.route('/customers')
def show_customer_data():
    # 模擬一些顧客資料
    customer_data = [
        {'customer_name': '顧客1', 'membership_level': 'VIP', 'contact': '123-456-7890', 'preferences': '偏好商品A', 'lifetime_value': '$500'},
        {'customer_name': '顧客2', 'membership_level': '一般會員', 'contact': '987-654-3210', 'preferences': '偏好商品B', 'lifetime_value': '$300'},
        {'customer_name': '顧客3', 'membership_level': 'VIP', 'contact': '111-222-3333', 'preferences': '偏好商品C', 'lifetime_value': '$700'},
        # 加入更多顧客資料...
    ]

    return render_template('customers.html', customers=customer_data)

if __name__ == '__main__':
    app.run(debug=True)
