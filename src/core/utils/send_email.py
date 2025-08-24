from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import aiosmtplib
import logging
import os


async def send_email(
    message_receiver: str,
    message_body: str,
    message_subject: str
) -> bool:
    load_dotenv()

    success = False
    
    sender_email = os.getenv("SENDER_EMAIL") 
    password = os.getenv("EMAIL_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = message_receiver
    message["Subject"] = message_subject
    message.attach(MIMEText(message_body, "plain"))
    
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")

    try:
        server = aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port)
        await server.connect()
        await server.starttls()
        await server.login(sender_email, password)
        await server.send_message(message)
        logging.info(f"message has been sent to: {message_receiver}")
        success = True
    except Exception as e:
        logging.warning(str(e))
    finally:
        await server.quit()
    
    return success



