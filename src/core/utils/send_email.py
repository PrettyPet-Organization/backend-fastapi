from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from email.mime.text import MIMEText
from dotenv import load_dotenv
import aiosmtplib
import logging
import os

load_dotenv()


async def send_email(
    message_receiver: str,
    message_body: str,
    message_subject: str
) -> bool:

    success = False
    
    sender_email = os.getenv("SENDER_EMAIL") 
    password = os.getenv("EMAIL_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = message_receiver
    message["Subject"] = message_subject
    message.attach(MIMEText(message_body, "plain"))
    
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))

    try:
        server = aiosmtplib.SMTP(
            hostname = smtp_server,
            port = smtp_port,
            start_tls = True
        )
        await server.connect()
        await server.login(sender_email, password)
        await server.send_message(message)
        logging.info(f"message has been sent to: {message_receiver}")
        success = True
    except Exception as e:
        logging.warning(str(e))
        raise HTTPException(
            detail = "something went wrong with verifying project",
            status_code = 500
        )
    finally:
        await server.quit()
    
    return success



