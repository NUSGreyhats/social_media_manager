import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_email(
    from_addr: str, to_addr: list[str], subject: str, body: str, cc: list[str] = []
) -> MIMEMultipart:
    """Create an email as a MIME object"""
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addr)
    msg["Cc"] = ", ".join(cc)
    msg["Subject"] = subject
    msg.attach(MIMEText(body))
    return msg


class EmailIntegration(object):
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        from_addr: str,
    ) -> None:
        """Initialize the email integration"""
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_addr = from_addr
        self.connection = None
        self._init_connection()

    def _init_connection(self) -> None:
        """Create the initial connection"""
        self.connection = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        self.connection.ehlo()
        self.connection.login(self.username, self.password)

    def send_email(self, to_email: str, email: MIMEMultipart) -> None:
        """Send an email"""
        if self.connection is None:
            self._init_connection()
        self.connection.sendmail(self.from_addr, [to_email], email.as_string())
