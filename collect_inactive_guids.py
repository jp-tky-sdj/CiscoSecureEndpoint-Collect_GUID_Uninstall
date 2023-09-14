from datetime import datetime
import requests
import csv
import configparser


# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read('config.ini')

BASE_URL_V1 = config['DEFAULT']['BASE_URL_V1']
CLIENT_ID = config['DEFAULT']['CLIENT_ID']
API_KEY_V1 = config['DEFAULT']['API_KEY_V1']

def calculate_time_delta(timestamp):
    '''Calculate how long it has been since the GUID was last seen
    '''
    time_format = '%Y-%m-%dT%H:%M:%SZ'
    datetime_object = datetime.strptime(timestamp, time_format)
    age = (datetime.utcnow() - datetime_object).days
    return age

def collect_inactive_guids(days_inactive):
    endpoint = f"{BASE_URL_V1}/computers/"
    
    # 認証の変更
    session = requests.Session()
    session.auth = (CLIENT_ID, API_KEY_V1)
    
    response = session.get(endpoint)
    
    
    # レスポンスのステータスコードを確認
    if response.status_code != 200:
        print(f"APIからのレスポンスが失敗しました。ステータスコード: {response.status_code}")
        print(response.text)
        return

    try:
        data = response.json()
        guids = [item['connector_guid'] for item in data['data']]
    except Exception as e:
        print(f"レスポンスの解析中にエラーが発生しました: {e}")
        print(response.text)
        return


    guids = []
    for item in data['data']:
        last_seen = item['last_seen']
        age = calculate_time_delta(last_seen)
        if age > days_inactive:
            guids.append(item['connector_guid'])

    # GUIDをCSVに保存
    with open('inactive_guids.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["GUID"])
        for guid in guids:
            writer.writerow([guid])

    print(f"{len(guids)}台の活動していない端末のGUIDをCSVに保存しました。")

days = int(input("何日以上活動がない端末の情報を収集しますか？: "))
collect_inactive_guids(days)
