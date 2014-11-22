from clients.bitcoin import Bitcoin
from settings.bitcoin import BITCOIN


class DefaultBitcoin(Bitcoin):
    def __init__(self):
        super(DefaultBitcoin, self).__init__(
            url=BITCOIN['api_url'],
            passphrase=BITCOIN['passphrase'],
        )
