import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.header import Header
from app.config import env_val


def send_email(data):
    smtp_server = "smtp.gmail.com"
    port = 465  # For starttls
    sender_email = env_val['MAIL_USERNAME']
    receiver_email = data['mahasiswa_email']
    password = env_val['MAIL_PASSWORD']
    SUBJECT = "Reset Password"

    msg = MIMEMultipart()
    # msg['From'] = "happymind@noreply"
    msg['From'] = formataddr((str(Header("Happy Mind No Reply", 'utf-8')), 'no_reply@example.com'))
    
    msg['To'] = data['mahasiswa_email']
    msg['Subject'] = SUBJECT
    msg.attach(MIMEText(f"""<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
  <div style="margin:50px auto;width:70%;padding:20px 0">
    <div style="border-bottom:1px solid #eee">
      <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Happy Mind</a>
    </div>
    <p style="font-size:1.1em">Hi,{receiver_email}</p>
    <p>Gunakan OTP berikut untuk menyelesaikan prosedur Lupa Password Anda. OTP berlaku selama 15 menit.</p>
    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{data['token']}</h2>
    <p style="font-size:0.9em;">Happy Mind</p>
    <hr style="border:none;border-top:1px solid #eee" />
   
  </div>
</div>"""
    , 'html'))


    context = ssl.create_default_context()


    with smtplib.SMTP_SSL(smtp_server, port,context=context) as server:
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    server.close()
