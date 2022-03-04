# WeatherAlerter : LINE Bot 風險天氣推播

每日接收氣象局 OpenAPI 最新預報資料，收到預報當日低溫或下雨資訊時，

LINE Bot 就會自動發出預警，天氣晴朗則不會發出警告。

## Setup
```
chmod +x ./get_cwb_weather.sh
chmod +x ./today_message.py
chmod +x ./linebot/push_alert_message.py
chmod +x ./linebot/app.py
```
* 設定 get_cwb_weather.sh 其中的 PROJECT_PATH
* 設定 get_cwb_weather.sh 中氣象局授權碼 AUTHORIZATION
* 設定 linebot/app.py  LINE Bot 的 CHENNEL_ACCESS_TOKEN  與 CHANNEL_SECRET
* crontab 中設定 get_cwb_weather.sh, today_message.py, linebot/push_alert_message.py 工作排程。

```
10 6 * * * <PROJECT_PATH>/get_cwb_weather.sh
15 6 * * * <PROJECT_PATH>/today_message.py
20 6 * * * <PROJECT_PATH>/linebot/push_alert_message.py
```
啟動 LINE Bot  
```
$ ./linebot/app.py
```

## Usage

### 管理者 

可透過 http://127.0.0.1:5000/send_message 向所有訂閱者發送訊息

### 用戶
訂閱 Line Bot 並發訊息以啟動預警服務。
輸入日期（ yyyy-mm-dd ）可查詢歷史天氣。





