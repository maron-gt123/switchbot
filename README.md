## switch bot APIを活用した湿温度計情報の定期監視
*  switch botのAPIを活用した電力/湿度/温度をGrafanaを用いて監視を実施する
  * 構築要件
    *  switch bot API 1.1を使用
    *  switch botのデバイスは自己解決
    *  本内容は監視を目的としており制御に関してはサポート外とする
  *  調達デバイスのIDを取得s
     * witchbot公式サイトからtoken及びsecretを確認[switchbot_token公式確認方法](https://support.switch-bot.com/hc/ja/articles/12822710195351-%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E5%8F%96%E5%BE%97%E6%96%B9%E6%B3%95)
     * 確認したtokenとsecretを以下のscriptの変数環境に代入し確認[switchbot_api_v11.sh](https://github.com/maron-gt123/switchbot/blob/main/switchbot_api_v11.sh)
     * switchbot_api_v11.shで取得したデバイスIDをもとにswitchbot_api_device_v11.shへ環境変数を追加し確認[switchbot_api_device_v11.sh](https://github.com/maron-gt123/switchbot/blob/main/switchbot_api_device_v11.sh)
  * Pythonを活用しデータを取得
   * 前提条件
     * influxDBを使いデータ管理
     * influxDBをインストール(2-2.6.1とする)

           # install influxdb
           wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.6.1-amd64.deb
           sudo dpkg -i influxdb2-2.6.1-amd64.deb
           wget https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.6.1-amd64.deb
           sudo dpkg -i influxdb2-client-2.6.1-amd64.deb
           rm influxdb2-2.6.1-amd64.deb
           rm influxdb2-client-2.6.1-amd64.deb

     * influx setupより初期設定を実施(設定横目は以下)

           $ influx setup
           > Welcome to InfluxDB 2.0!
           ? Please type your primary username <ユーザ名>
           ? Please type your password <パスワード>
           ? Please type your password again <パスワード>
           ? Please type your primary organization name <組織名>
           ? Please type your primary bucket name <defaultデータベース名>
           ? Please type your retention period in hours, or 0 for infinite 0
     * Python3をインストール

           apt install python3
   * Python3をインストール
  * ｄｖｄｓ
