import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# coding: utf-8


alert = 'sin_mirror'
toaddr= 'avishayafik@gmail.com'
subject='restart was done ' + alert



class email():
    def __init__(self,toaddr,subject,fromaddr,smtp,smtp_port,username,password,email_message):
        #self.alert = alert
        self.toaddr = toaddr
        self.subject = subject
        self.fromaddr = fromaddr
        self.smtp = smtp
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.email_message = email_message
        #self.email_message = email_message

    def send_email(self):
        space = " "
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = self.toaddr
        msg['Subject'] = self.subject
        body = ""
        p = MIMEBase('application', 'octet-stream')
        # creates SMTP session
        try:
            s = smtplib.SMTP(self.smtp, self.smtp_port)
            s.starttls()
            s.login(self.username, self.password)
            # Converts the Multipart msg into a string
            text = msg.as_string()
            # sending the mail
            s.sendmail(self.fromaddr, self.toaddr.split(','),text)
            # print "sent email successfully"
        except Exception:
            pass

    def send_email_html(self,color):
        space = " "
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = self.toaddr
        msg['Subject'] = self.subject
        body = ""
        p = MIMEBase('application', 'octet-stream')
        if color == "green":
            html = """\
            <!DOCTYPE html>
            <html>
               <body style="background-color:green;">
                  <p>    </p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <h1>"%s"</h1>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p>      </p>
               </body>
            </html>
            """ % (self.email_message)
        else:
            html = """\
            <!DOCTYPE html>
            <html>
               <body style="background-color:red;">
                  <p>    </p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <h1>"%s"</h1>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p></p>
                  <p>     </p>
               </body>
            </html>
            """ % (self.email_message)
        HTML_BODY = MIMEText(html, "html")
        msg.attach(HTML_BODY)
        # creates SMTP session
    #try:
        s = smtplib.SMTP(self.smtp, self.smtp_port)
        s.starttls()
        s.login(self.username, self.password)
        # Converts the Multipart msg into a string
        message = msg.as_string(msg)
        # sending the mail
        s.sendmail(self.fromaddr, self.toaddr.split(','),message)
                # print "sent email successfully"
     #   except Exception:
     #       pass
