from settings.bitsplit import BITSPLIT
from mailer import Message, Mailer


class Email(Message):
    def __init__(self, *args, **kwargs):
        kwargs['From'] = BITSPLIT['email_from']
        kwargs["To"] = BITSPLIT['email_to']
        super(Email, self).__init__(*args, **kwargs)

    def send(self):
        sender = Mailer(
            host=BITSPLIT['smtp_host'],
            port=BITSPLIT['smtp_port'],
            use_tls=BITSPLIT['smtp_tls'],
            usr=BITSPLIT['smtp_username'],
            pwd=BITSPLIT['smtp_password'],
        )
        sender.send(self)
