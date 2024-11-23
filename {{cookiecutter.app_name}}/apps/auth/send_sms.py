def send_otp_message(phone, code):
    print(f"phone::{phone}=> code::{code}")
    Thread(target=sms, args=(phone, code)).start()

def sms(_phone, _message):
    url = "https://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber"

    payload = f'username=09117507790&password=BOD%40E&text={_message}&to={_phone}&bodyId=151748'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
