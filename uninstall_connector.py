import requests
import csv
import configparser

# 設定ファイルを読み込む
config = configparser.ConfigParser()
config.read('config.ini')

BASE_URL_V3 = config['DEFAULT']['BASE_URL_V3']
ACCESS_TOKEN_V3 = config['DEFAULT']['ACCESS_TOKEN_V3']
ORGANIZATION_ID = config['DEFAULT']['ORGANIZATION_ID']

def uninstall_connector_from_guids():
    with open('inactive_guids.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            guid = row[0]
            endpoint = f"{BASE_URL_V3}/organizations/{ORGANIZATION_ID}/computers/{guid}/uninstall_request"
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN_V3}"
            }
            response = requests.put(endpoint, headers=headers)
            if response.status_code == 204:
                print(f"GUID {guid} のコネクタをアンインストールのリクエストを送信しました。")
            else:
                print(f"GUID {guid} のコネクタのアンインストールリクエストに失敗しました。エラーコード: {response.status_code}")

uninstall_connector_from_guids()

