from clients.counterparty import Counterparty
from settings.counterparty import COUNTERPARTY


class DefaultCounterparty(Counterparty):
    def __init__(self):
        super(DefaultCounterparty, self).__init__(
            api_url=COUNTERPARTY['api_url'],
            user=COUNTERPARTY['user'],
            password=COUNTERPARTY['password'],
        )
