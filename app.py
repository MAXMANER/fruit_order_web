from flask import Flask, render_template, request, redirect, url_for
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
app = Flask(__name__)

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
        return '請聯絡管理員,q1'

@app.route('/text')
def text():
    return '<html><body><h1>我們已收到您的訂單，感謝您的訂購</h1></html>'


@app.route('/home', methods=['GET', 'POST'])
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
                line_bot_api = LineBotApi('VHR1ncoqHEos96MftVkgoidjhC7Aeiwo/c5NsxrAmrICpHNgP+nKte9tpimRlz4+Vsnuo1vn/fbjFkqh47KKJlbBmjAKN0x2RTvCgvu5L0LmunPJhpUa18g5oeuzznPLR+pYclbg8cPuq7WTNCbuYwdB04t89/1O/w1cDnyilFU=')
                profile = line_bot_api.get_profile(user_id)        
            #if user_id != None:
                return render_template('index.html',user_id = user_id ,user_name = profile.display_name)
            else:
                return '請聯絡管理員,q2'
    except Exception as e:
        print(e)
        return '請聯絡管理員,q1'


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


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
    
