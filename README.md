# CiscoSecureEndpoint-Collect_GUID_Uninstall
Cisco Systems の EPP/EDR製品に分類される Cisco Secure Endpoint の公開されている APIを利用して、そのコネクター（エージェントソフトウェア）のうち活動が見られないものを探し出しアンインストールのリクエストを送るスクリプトのサンプルです。
指定日数観測されないGUIDの情報をCSVファイルにアウトプットする collect_inactive_guids.py と、そのCSVにリストされたGUIDを持つコネクター（エージェント）を一括で端末からアンインストールするようAPIでリクエストする uninstall_connector.py という二つのスクリプトに分けて作成しています。

# config.ini の準備
collect_inactive_guids.py は Secure Endpoint　の API エンドポイントのバージョン1で動作します。この API エンドポイントにおける認証方法は Basic　認証です。
config.ini にある、以下の太字の部分は

CLIENT_ID = **YOUR_API_CLIENT_ID_from_API-Credential**
API_KEY_V1 = **YOUR_API_KEY_for_API_CLIENT_ID** 

以下のコミュニティ記事の 「1.APIクレデンシャルの作成」にて紹介されている方法で取得した値に書き換えて保存します。

**参考： Cisco AMP for Endpoints APIの使い方について**

https://community.cisco.com/t5/-/-/ta-p/3220035

APJCにビジネスを持つユーザの場合 API エンドポイントは以下の ”apjc" という文字列がURLに含まれたものになっていると想定しています。

**BASE_URL_V1 = https://api.apjc.amp.cisco.com/v1**

これら３つの変数を、自身の環境の値に書き換えれば collect_inactive_guids.py は動作しCSVを出力します。

出力されたCSVに含まれるGUIDのリストを利用し、コネクターのアンインストールをリクエストするには、APIのバージョン3が利用されます。
このAPIv3はトークンを元にした認証となり、APIv0, APIv1と認証方法が異なっております。
このAPIv3でトークンを取得するには、まずSecureXからClient IDとClient Password　を取得する必要があります。
まず SecureX にログインし [Administration] タブから [API Clients] に移動し、”Generate API　Client” をクリックします。
ここで発行される Client ID と Client Password を保存します。
getaccesstoken.sh を実行すると、client ID と client secret を問われるので、今取得した Client ID と Client Password をそれぞれ入力します。すると **access_token** と **organization** が含まれた結果が返ってきます。これを config.ini　の **ACCESS_TOKEN_V3** と
**ORGANIZATION_ID** の値として書き換え保存します。
※トークンには有効期間があることに注意してください。
この **getaccesstoken.sh** は以下の Cisco Developer　のサイトを参考にして再編したスクリプトで、APJCのビジネスで動作するものとなっています。

**参考： Cisco Developer > Secure Endpoint API > Authentication**

https://developer.cisco.com/docs/secure-endpoint/#!authentication/3-generate-securex-api-access-token

このスクリプトとは直接関係はないですが、以下の日本語によるコミュニティ記事も紹介します。
**参考： [Secure Endpoint] Postmanを使ったSecure Endpoint API v3のテスト方法**

https://community.cisco.com/t5/-/-/ta-p/4704030

これで config.ini の変数を全て自身の環境の値に書き換えて保存すれば準備は完了です。

# collect_inactive_guids.py の実行

`python3 collect_inactive_guids.py `

と実行すると、
「何日以上活動がない端末の情報を収集しますか？:」
と問われるので、半角数字で入力します。回答した日数以上活動の見られないコネクタのGUIDを集め同じディレクトリにCSV形式でアウトプットします。

# uninstall_connector.py の実行
次に、このCSVファイルが同じディレクトリにある状態でuninstall_connector.pyを

`python3 uninstall_connector.py`

というように実行すると、CSVに記載のあるGUIDを持つコネクタに対して、アンインストールをリクエストします。



