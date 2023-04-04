from app.database import db #, event database, events
from app import app
from datetime import datetime
import asyncio
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



message= MIMEMultipart("alternative")
smtp_server='smtp.gmail.com'
smtp_port=465
sender= 'sender@gmail.com'
password='password'
subject='Incoming events'
context = ssl.create_default_context()
html="""
HTML code here
"""
text= "Your event(s) starts in 3 days"
mess1=MIMEText(text, "plain")
mess2 = MIMEText(html, "html")
message.attach(mess1)
message.attach(mess2)

async def daily_email_check():
    event= events.query.filter_by(Time_Stamp=datetime.date.today()+datetime.timedelta(days=3)).all()
    recievers=event.email
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls(context=context)
    TIE_server.login(sender, password)
    
    for reciever in recievers:
        TIE_server.sendmail(sender, reciever, message.as_string())
        print(f"Email successfully sent to - {reciever}")
    
    TIE_server.quit()
    
    await asyncio.sleep(24*60*60)
