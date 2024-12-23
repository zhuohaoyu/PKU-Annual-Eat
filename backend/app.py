from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
CORS(app)

def analyze_special_transactions(transactions):
    # Filter dining transactions (negative amounts)
    dining_transactions = [t for t in transactions if t["TRANAMT"] < 0]
    
    # Early birds (5:00-7:00)
    early_birds = [t for t in dining_transactions if 5 <= datetime.strptime(t["OCCTIME"], "%Y-%m-%d %H:%M:%S").hour < 7]
    early_birds.sort(key=lambda x: datetime.strptime(x["OCCTIME"], "%Y-%m-%d %H:%M:%S"))
    
    # Night owls (21:00-23:59)
    night_owls = [t for t in dining_transactions if datetime.strptime(t["OCCTIME"], "%Y-%m-%d %H:%M:%S").hour >= 21]
    night_owls.sort(key=lambda x: datetime.strptime(x["OCCTIME"], "%Y-%m-%d %H:%M:%S"), reverse=True)
    
    # Big spenders (top 5 largest transactions)
    big_spenders = sorted(dining_transactions, key=lambda x: abs(x["TRANAMT"]), reverse=True)
    
    return {
        "early_birds": early_birds[:5],
        "night_owls": night_owls[:5],
        "big_spenders": big_spenders[:5]
    }

@app.route('/api/report', methods=['POST'])
def generate_report():
    try:
        data = request.json
        account = data.get('account')
        hallticket = data.get('hallticket')
        session_id = data.get('sessionId')
        sdate = data.get('sdate')
        edate = data.get('edate')
        
        if not all([account, hallticket, session_id, sdate, edate]):
            logger.error("Missing required parameters")
            return jsonify({'error': '请提供完整的信息'}), 400

        # Call campus card API with all headers
        url = "https://card.pku.edu.cn/Report/GetPersonTrjn"
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://card.pku.edu.cn',
            'Referer': 'https://card.pku.edu.cn/Page/Page',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }
        
        cookies = {
            "hallticket": hallticket,
            "ASP.NET_SessionId": session_id
        }
        
        post_data = {
            "sdate": sdate,
            "edate": edate,
            "account": account,
            "page": "1",
            "rows": "9000",
        }
        
        response = requests.post(url, headers=headers, cookies=cookies, data=post_data)

        if not response.ok:
            return jsonify({'error': '获取数据失败'}), 400

        data = response.json()
        if not data.get('rows'):
            return jsonify({'error': '未找到交易记录'}), 404

        transactions = data["rows"]
        
        # Filter dining transactions
        dining_transactions = [t for t in transactions if float(t["TRANAMT"]) < 0]
        
        # Calculate consumption by location
        all_data = {}
        for item in dining_transactions:
            try:
                merc_name = item["MERCNAME"].strip()
                if merc_name in all_data:
                    all_data[merc_name] += abs(float(item["TRANAMT"]))
                else:
                    all_data[merc_name] = abs(float(item["TRANAMT"]))
            except Exception:
                continue

        all_data = {k: round(v, 2) for k, v in all_data.items()}
        
        # Generate summary
        summary = {
            "total_categories": len(all_data),
            "total_transactions": len(dining_transactions),
            "total_amount": round(sum(all_data.values()), 2)
        }

        # Analyze special transactions
        special_transactions = analyze_special_transactions(transactions)

        return jsonify({
            'summary': summary,
            'consumption_data': all_data,
            'transactions': dining_transactions,
            'special_transactions': special_transactions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 