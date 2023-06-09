import requests

def send_line_notify(notification_message):
    """
    LINEに通知する
    """

    # リストから、文字列へ変換する
    data_list = ""
    for value in notification_message:
        data_list = data_list + "\n" + value

    line_notify_token = 'トークンを記載する'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f' {data_list}'}
    requests.post(line_notify_api, headers = headers, data = data)
