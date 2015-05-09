import smtplib
import os 

smtpUser = os.environ.get('SMTP_USER')
smtpPass = os.environ.get('SMTP_PASSWORD')

toAdd = os.environ.get('NOTIFY_USER_EMAIL')

fromAdd = smtpUser
subject = 'Python Test'
header = "to: "
body = "Python script"

s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()

s.login(smtpUser,smtpPass)
s.sendmail(fromAdd,toAdd,header + '\n' + body)
s.quit()
