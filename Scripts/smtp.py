import pathlib
import smtplib
import private as prv
from email.mime.image import MIMEImage

sent_from = 'tomatotracker.business@gmail.com'
to = ['tomatotracker.business@gmail.com']
subject = 'Toato Tracker Message'
body = "Hey, what's up?\n\n- You"

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    print(1)
    print(prv.getEmail())
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print ('Email sent!')
except:
    print ('Something went wrong...')

# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.multipart import MIMEMultipart


# def SendMail(ImgFileName):
#     img_data = open(ImgFileName, 'rb').read()
#     msg = MIMEMultipart()
#     msg['Subject'] = 'Tomato Tracker'
#     msg['From'] = 'conorgpower'
#     msg['To'] = 'e@mail.cc'

#     text = MIMEText("test")
#     msg.attach(text)
#     image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
#     msg.attach(image)

#     s = smtplib.SMTP(Server, Port)
#     s.ehlo()
#     s.starttls()
#     s.ehlo()
#     s.login(UserName, UserPassword)
#     s.sendmail(From, To, msg.as_string())
#     s.quit()