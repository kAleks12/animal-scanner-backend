import logging
import pathlib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

from src.utils.config_parser import parser
import smtplib


class EmailSender:
    def __init__(self):
        self.logger = logging.getLogger("Email-Sender")
        self.__reset_url = parser.get_attr("email", "reset_url")
        self.__register_url = parser.get_attr("email", "register_url")
        self.__sender_name = parser.get_attr("email", "sender_name")
        self.__server = parser.get_attr("email", "smtp_server")
        self.__port = parser.get_attr("email", "smtp_port")
        self.__user = parser.get_attr("email", "user")
        self.__password = parser.get_attr("email", "password")

    def __prepare_reset_password_html(self, receiver: str, reset_code: str, exp_delta: int) -> str:
        with open(f"{pathlib.Path(__file__).parent.resolve()}\\templates\\reset_password_en.html", "r") as template:
            html = template.read()
            return (
                html.replace("{exp_delta}", str(exp_delta))
                .replace("{url}", f"{self.__reset_url}{reset_code}")
                .replace("{name}", receiver)
            )

    def __prepare_register_html(self, receiver: str, activation_code: str) -> str:
        with open(f"{pathlib.Path(__file__).parent.resolve()}\\templates\\register_en.html", "r") as template:
            html = template.read()
            return (
                html.replace("{url}", f"{self.__register_url}{activation_code}")
                .replace("{name}", receiver)
            )

    def send_reset_password(self, receiver: str, reset_code: str, exp_delta: int) -> None:
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Reset Password"
            message["From"] = self.__sender_name
            message["To"] = receiver
            message.attach(MIMEText(self.__prepare_reset_password_html(receiver, reset_code, exp_delta), "html"))

            sender_thread = Thread(target=self._send_email_async,
                                   args=[self.__server, self.__port, self.__user, self.__password, self.__sender_name,
                                         receiver, message])
            sender_thread.start()
        except Exception as e:
            self.logger.exception("Failed to send reset password email")
            self.logger.exception(e)
            raise

    def send_register(self, receiver: str, activation_code: str) -> None:
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Activate your account"
            message["From"] = self.__sender_name
            message["To"] = receiver
            message.attach(MIMEText(self.__prepare_register_html(receiver, activation_code), "html"))

            sender_thread = Thread(target=self._send_email_async,
                                   args=[self.__server, self.__port, self.__user, self.__password, self.__sender_name,
                                         receiver, message])
            sender_thread.start()
        except Exception as e:
            self.logger.exception("Failed to send register email")
            self.logger.exception(e)
            raise

    def _send_email_async(self, server, port, user, password, sender_name, receiver, message):
        try:
            with smtplib.SMTP_SSL(server, port, context=ssl.create_default_context()) as server:
                server.login(user, password)
                server.sendmail(sender_name, receiver, message.as_string())
        except Exception as e:
            self.logger.exception("Failed to send register email")
            self.logger.exception(e)


sender = EmailSender()
