import smtplib
import string
 
import settings

def send_new_user_notification(to_email, token):
    SUBJECT = "[auth] Account Activation"
    text = "Welcome! please activate your account with the code: %s" % token
    BODY = string.join((
            "From: %s" % settings.EMAIL_FROM,
            "To: %s" % to_email,
            "Subject: %s" % SUBJECT ,
            "",
            text
            ), "\r\n")
    server = smtplib.SMTP(settings.EMAIL_HOST)
    server.sendmail(settings.EMAIL_FROM, [to_email], BODY)
    server.quit()

