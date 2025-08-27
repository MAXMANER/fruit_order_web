from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
app = Flask(__name__)

access_token = 'jbpfRdbeAfDT3y1qz/1rJwPL64uq4DyMQPU6jYMkWXP8fWs/r70U594KVq53n7/urPvZXEywJTVhRIjnz2Cr14VwT5Y7uiX5+mENfVOYALF7u7JzMmcTGTotzklae3Lz000XXwSrR3eNQvv7mSiCCAdB04t89/1O/w1cDnyilFU='
save_data_url = 'http://127.0.0.1:4999'
#access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
#save_data_url = os.getenv('SAVE_DATA_URL')
@app.route("/")
def index():
  try:
    msg = request.args.get('msg')   # 取得網址的 msg 參數
    return 'OKK'

  except:
    return 'error'
    print('error')

@app.route('/hello')
def hello():
    return 'Hello World '


@app.route('/test')
def test():
    try:
        msg = request.args.get('id')   
        if msg != None:
            return render_template('index.html',)
        else:
            return '請聯絡管理員,q2'
    except Exception as e:
        print(e)
        return f'請聯絡管理員,q1'

@app.route('/qrcode_page')
def qrcode_page():
    user_id = request.args.get('user_id')   
    #user_name = request.args.get('user_name') 
    if user_id != None:
        line_bot_api = LineBotApi(access_token)
        profile = line_bot_api.get_profile(user_id)        
        return render_template('qrcode_page.html',user_id = user_id ,user_name = profile.display_name)
    else:
        return '請聯絡管理員,q2'

#@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        print(request.method)
        if request.method == 'POST':
            print('It is post')
            return 'It is post'
            #return redirect(url_for('static'))
        else:    
            user_id = request.args.get('user_id')   
            #user_name = request.args.get('user_name') 
            if user_id != None:
                line_bot_api = LineBotApi(access_token)
                profile = line_bot_api.get_profile(user_id)   
                #sender = fetch_sender(user_id)
                quantity = fetch_quantity()
                purchaser_data = fetch_purchaser_data(user_id)
                for item in purchaser_data:
                    print(item)
                #sender_name = sender['sender_name'] if  sender['sender_name'] else ""
                #sender_phone = sender['sender_phone'] if  sender['sender_phone'] else ""
                item1_quantity = quantity['item1_quantity'] if  quantity['item1_quantity'] else 0
                item2_quantity = quantity['item2_quantity'] if  quantity['item2_quantity'] else 0
                item3_quantity = quantity['item3_quantity'] if  quantity['item3_quantity'] else 0

                return render_template('order_page.html',user_id = user_id ,user_name = profile.display_name,save_data_url = save_data_url,sender_name = "", sender_phone = "", item1_max_quantity = item1_quantity,item2_max_quantity = item2_quantity,item3_max_quantity = item3_quantity, data_list = purchaser_data)
            else:
                return '請聯絡管理員,q2'
    except Exception as e:
        print(e)
        return '請聯絡管理員,q1'

# ===== 你原本的 /home：改成不再傳 item1/item2，用 item_api_url 動態取品項 =====
@app.route('/order_page', methods=['GET', 'POST'])
def order_page():
    try:
        print(request.method)
        if request.method == 'POST':
            print('It is post')
            return 'It is post'
            # return redirect(url_for('static'))

        # GET:
        user_id = request.args.get('user_id')
        if user_id is None:
            return '無法取得 user_id，請聯絡管理員'

        # 取得使用者暱稱（失敗時退回空字串，不中斷流程）
        try:
            line_bot_api = LineBotApi(access_token)  # 你原本的 access_token
            profile = line_bot_api.get_profile(user_id)
            user_name = profile.display_name or ""
        except Exception as e:
            print("get_profile error:", e)
            user_name = ""

        # 歷史收件人資料（維持你原本的函式）
        purchaser_data = fetch_purchaser_data(user_id) or []

        # ✅ 關鍵改動：不再在這裡處理 item1/item2 的庫存
        #    前端將改呼叫 /api/items 取得任意數量的動態品項

        return render_template(
            'order_page_beautified.html',
            user_id=user_id,
            user_name=user_name,
            # 前端會 fetch 這個 API 來動態產生商品卡片
            save_data_url = save_data_url,
            item_api_url=f'{save_data_url}/api/items',
            # 歷史資料仍可供選擇
            data_list=purchaser_data,
            # 舊版模板若仍引用這些變數，不想大改的話可以先給 0，避免渲染錯誤
            item1_max_quantity=0,
            item2_max_quantity=0,
            item3_max_quantity=0,
        )
    except Exception as e:
        print(e)
        return '請聯絡管理員,q1'




# =====（可選）新增：前端 AJAX 儲存訂單資料的接收端點 =====
@app.post('/order/save_data')
def save_data():
    """
    與前端的 save_data_url 對應：
    前端會 POST 到  {{ save_data_url }}/save_data  => /order/save_data
    請在這裡完成：
      1) 檢核庫存（針對每個 item_id 扣量；需做交易/鎖，避免超賣）
      2) 寫入訂單與訂單項目
      3) 回傳 200/201
    """
    try:
        payload = request.get_json(silent=True) or {}
        print("save_data payload:", payload)

        # TODO: 在這裡完成
        # - 交易開始
        # - 寫入 orders, order_items
        # - 扣庫存（以 item_id 為主，扣 payload['groups'][0]['items'][*]['quantity']）
        # - 交易提交

        return jsonify({"ok": True}), 200
    except Exception as e:
        print("save_data error:", e)
        return jsonify({"ok": False, "error": str(e)}), 500
# ========================================================

@app.route('/page/text')
def pageText():
    return render_template('page.html', text="Python Flask !")


@app.route('/page/app')
def pageAppInfo():
    appInfo = {  # dict
        'id': 5,
        'name': 'Python - Flask',
        'version': '1.0.1',
        'author': 'Enoxs',
        'remark': 'Python - Web Framework'
    }
    return render_template('page.html', appInfo=appInfo)


@app.route('/page/data')
def pageData():
    data = {  # dict
        '01': 'Text Text Text',
        '02': 'Text Text Text',
        '03': 'Text Text Text',
        '04': 'Text Text Text',
        '05': 'Text Text Text'
    }
    return render_template('page.html', data=data)


@app.route('/static')
def staticPage():
    return render_template('static.html')

'''
def fetch_sender(user_id):
    try:fetch_sender
        # Make the GET request to the server API with parameters
        response = requests.get(f'{save_data_url}/get_sender?purchaser_id={user_id}')
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        print(data)
        return data
        # Return the data as a JSON response
    except requests.exceptions.RequestException as e:
        print({'error': str(e)})
        return 'error'
'''

def fetch_quantity():
    try:
        # Make the GET request to the server API with parameters
        response = requests.get(f'{save_data_url}/get_quantity')
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        #print(data)
        return data
        # Return the data as a JSON response
    except requests.exceptions.RequestException as e:
        print({'error': str(e)})
        return 'error'

def fetch_purchaser_data(purchaser_id):
    try:
        # Make the GET request to the server API with parameters
        response = requests.get(f'{save_data_url}/get_purchaser_data?purchaser_id={purchaser_id}')
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        data = data["data"]
        return data
        # Return the data as a JSON response
    except requests.exceptions.RequestException as e:
        print({'error': str(e)})
        return 'error'

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
    
