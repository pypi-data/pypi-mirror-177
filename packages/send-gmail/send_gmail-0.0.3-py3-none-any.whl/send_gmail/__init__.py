from dataclasses import dataclass, field
from datetime import datetime
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.charset import Charset, QP
from os.path import basename



@dataclass
class SendGMail:
    """ Sending an email via smtp Server, defaults to smtp.gmail.com with port 465
    """
    id:str
    pwd:str
    smtp:str = field(default='smtp.gmail.com')
    port:int = field(default=465)



    def _create_attachment(self,filename:str) -> MIMEBase:
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                # Set mail headers
                part.add_header(
                    "Content-Disposition",
                    "attachment", filename= basename(filename)
                )
                return part
        except:
            return None
    


    def send(self, from_addr:str, 
                    to_addr:str, 
                    subject:str=None,
                    html:str=None,
                    text:str=None, 
                    attachments:(list|str)=None 
                    ) -> dict:  
        """send an email, main routine

        Args:
            from_addr (str | None): sender email, if None the id field is used   
            to_addr (list | str): receiver(s) email, string for one - list for many
            subject (str | None ): subject as utf-8 text, if None current date is send
            html (str, optional):html part of message. Defaults to None.
            text (str, optional): text part of message. Defaults to None.
            attachments (list | str, optional): files to attach. Defaults to None.

        Returns:
            dict: dictionary of errors, key == to_addr, value == Error
        """
        # possible values, alternative, mixed
        parttype = "mixed"
        # no text and html we set text to empty string
        if not text and not html:
            text = ''
        elif text and html:
            parttype = "alternative"

        subparts = []
        # attach the provided content    
        charset = Charset("utf-8")
        charset.header_encoding = QP
        charset.body_encoding = QP

        if text != None:
            subparts.append(MIMEText(_text=text,_subtype="plain",_charset=charset))
        # last MIMEText is the default - order matters
        if html:
            subparts.append(MIMEText(_text=html,_subtype="html",_charset=charset)) 

        if attachments:
            if isinstance(attachments,str):
                attachments = [attachments]
            for attachment in attachments:
                if (part := self._create_attachment(attachment)):
                    subparts.append(part)   

        msg:MIMEMultipart = MIMEMultipart(_subtype=parttype,_subparts=subparts)
        if subject == None:
            subject = datetime.now().replace(microsecond=0).isoformat()  
        msg["Subject"] = subject.strip() 
        msg["From"] = from_addr if from_addr else self.id
        msg["To"] = to_addr if isinstance(to_addr,str) else '; '.join(to_addr)
     
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp,self.port, context=context) as server:
            server.login(self.id,self.pwd)
            errs = server.sendmail(from_addr=msg["From"],to_addrs=to_addr,msg=msg.as_string())
            return errs

