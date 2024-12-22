import json
import matplotlib.pyplot as plt
import requests
import platform

account = ""
hallticket = ""
all_data = dict()

if __name__ == "__main__":
    # 读入账户信息
    try:
        with open("config.json", "r", encoding='utf-8') as f:
            config = json.load(f)
            account = config["account"]
            hallticket = config["hallticket"]
    except Exception as e:
        print("账户信息读取失败，请重新输入")
        account = input("请输入account: ")
        hallticket = input("请输入hallticket: ")
        with open("config.json", "w", encoding='utf-8') as f:
            json.dump({"account": account, "hallticket": hallticket}, f, indent=4)
    
    # 发送请求，得到加密后的字符串
    url = f"https://card.pku.edu.cn/Report/GetPersonTrjn"
    cookie = {
        "hallticket": hallticket,
    }
    post_data = {
        "sdate": "2020-01-01",
        "edate": "2024-12-31",
        "account": account,
        "page": "1",
        "rows": "9000",
    }
    response = requests.post(url, cookies=cookie, data=post_data)

    data = json.loads(response.text)["rows"]

    # 整理数据
    for item in data:
        try:
            if(item["TRANAMT"] < 0):
                if item["MERCNAME"].strip() in all_data:
                    all_data[item["MERCNAME"].strip()] += abs(item["TRANAMT"])
                else: 
                    all_data[item["MERCNAME"].strip()] = abs(item["TRANAMT"])
        except Exception as e:
            pass
    all_data = {k: round(v, 2) for k, v in all_data.items()}
    summary = f"统计总种类数：{len(all_data)}\n总消费次数：{len(data)}\n总消费金额：{round(sum(all_data.values()), 1)}"
    print(summary)
    # 输出结果
    all_data = dict(sorted(all_data.items(), key=lambda x: x[1], reverse=False))
    if len(all_data) > 50:
        # Get top 10 and bottom 10
        top_10 = dict(list(all_data.items())[:20])
        bottom_10 = dict(list(all_data.items())[-20:])
        # Add a separator between top and bottom groups
        middle_values = list(all_data.values())[20:-20]
        separator = {"中间省略": sum(middle_values)}  # Sum of middle values
        all_data = {**top_10, **separator, **bottom_10}
    
    if platform.system() == "Darwin":
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    elif platform.system() == "Linux":
        plt.rcParams['font.family'] = ['Droid Sans Fallback', 'DejaVu Sans']
    else:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        
    plt.figure(figsize=(12, len(all_data) / 66 * 18))
    plt.barh(list(all_data.keys()), list(all_data.values()))
    for index, value in enumerate(list(all_data.values())):
        plt.text(value + 0.01 * max(all_data.values()),
                index,
                str(value),
                va='center')
        
    # plt.tight_layout()
    plt.xlim(0, 1.2 * max(all_data.values()))
    plt.title(f"白鲸大学食堂消费情况\n({post_data['sdate']} 至 {post_data['edate']})")
    plt.xlabel("消费金额（元）")
    plt.text(0.8, 0.1, summary, ha='center', va='center', transform=plt.gca().transAxes)
    plt.savefig("result.png")
    plt.show()
