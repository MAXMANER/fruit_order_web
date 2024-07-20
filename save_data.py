from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MAXMANYO2",
        database="jumanage"
    )

@app.route('/save_data', methods=['POST'])
def save_data():
    purchaser_id = request.form['purchaser_id']
    purchaser_name = request.form['purchaser_name']
    recipient_name = request.form['recipient_name']
    recipient_phone = request.form['recipient_phone']
    recipient_address = request.form['recipient_address']
    sender_name = request.form['sender_name']
    sender_phone = request.form['sender_phone']
    total_price = request.form['total_price']
    item1_quantity = int(request.form['item1_quantity'])
    item2_quantity = int(request.form['item2_quantity'])
    conn = connect_db()
    cursor = conn.cursor()
    date = datetime.now()
    print(f'total_price: {total_price}')
    try:
        sql = "INSERT INTO ju_order_full (purchaser_id, purchaser_name,recipient_name,recipient_phone,recipient_address,sender_name,sender_phone,total_price,create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (purchaser_id, purchaser_name,recipient_name,recipient_phone,recipient_address,sender_name,sender_phone,total_price,date)
        print(sql)
        cursor.execute("INSERT INTO ju_order_full (purchaser_id, purchaser_name,recipient_name,recipient_phone,recipient_address,sender_name,sender_phone,total_price,create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (purchaser_id, purchaser_name,recipient_name,recipient_phone,recipient_address,sender_name,sender_phone,total_price,date))
        conn.commit()
        generated_id = cursor.lastrowid
        print(generated_id)
        # item1 using the generated ID
        if item1_quantity > 0:
            item1_query = "INSERT INTO ju_order_dtl (order_id, item_id, quantity) VALUES (%s, %s, %s)"
            item1_values = (generated_id, 1, item1_quantity)
            cursor.execute(item1_query, item1_values)
            conn.commit()

        # item2 using the generated ID
        if item2_quantity > 0:
            item2_query = "INSERT INTO ju_order_dtl (order_id, item_id, quantity) VALUES (%s, %s, %s)"
            item2_values = (generated_id, 2, item2_quantity)
            cursor.execute(item2_query, item2_values)
            conn.commit()

        return jsonify({'status': 'success', 'id': generated_id})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/api/data', methods=['GET'])
def get_data_test():
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    
    # Example response data using the parameters
    data = {
        'param1': param1,
        'param2': param2,
        'message': f"Received param1: {param1} and param2: {param2}"
    }
    
    return jsonify(data), 200

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()
        #purchaser_id = request.form['purchaser_id'] 
        purchaser_id = request.args.get('purchaser_id')
        print(purchaser_id)
        #get total pirce
        query = "SELECT SUM(total_price) FROM ju_order_full WHERE purchaser_id=%s"
        value = (purchaser_id,)
        cursor.execute(query,value)
        total_price = cursor.fetchall()

        # Query to get data from the table
        query = "SELECT ju_order_dtl.item_id, ju_order_dtl.name,SUM(ju_order_dtl.quantity) AS quantity from ju_order_full  LEFT JOIN (SELECT ORDER_id,ju_order_dtl.item_id,ju_order_dtl.quantity,item.name from ju_order_dtl inner JOIN item ON order_id WHERE ju_order_dtl.item_id=item.item_id) as ju_order_dtl ON ju_order_full.order_id = ju_order_dtl.order_id WHERE ju_order_full.purchaser_id= %s GROUP BY ju_order_dtl.item_id ORDER BY ju_order_dtl.item_id "
        #query = "SELECT item_id,SUM(quantity) FROM  ju_order_dtl where order_id IN (SELECT order_id from ju_order_full WHERE purchaser_id='U4b5c9276aa1f7a88223db89bfb8569fc') GROUP BY item_id"
        value = (purchaser_id,)
        #cursor.execute(query)
        cursor.execute(query,value)
        results = cursor.fetchall()

        # Get column names
        # column_names = [desc[0] for desc in cursor.description]
        # Combine column names with rows
        # users = [dict(zip(column_names, row)) for row in results]
        item={}
        for row in results:
            item[row[0]]=row[2]
        return jsonify({'status': 'success', 'item': item,'total_price' : total_price[0][0]})
    
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)})
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=4998)
