from aiosmtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText


class Email(object):
    def __init(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    async def async_send(self, email, subject, content):
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'], message['To'] = self.username, email
        message['Subject'] = Header(subject, 'utf-8')
        async with SMTP(hostname=self.host, port=self.port, use_tls=True) as smtp:
            await smtp.login(message['From'], self.password)
            await smtp.send_message(message)
        return True
