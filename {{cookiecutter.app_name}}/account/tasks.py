from celery import shared_task
from account.send_sms import send_otp_message


@shared_task()
def otp_password(phone, code):
    send_otp_message(phone=phone, code=code)
