from bitcoinrpc.authproxy import AuthServiceProxy


class Bitcoin(object):
    def __init__(self, url, passphrase):
        self.url = url
        self.passphrase = passphrase
        self._connect()

    def _connect(self):
        self.conn = AuthServiceProxy(self.url)

    def get_info(self):
        return self.conn.getinfo()

    def get_balance(self, address):
        balance = self.conn.getbalance(address)

        if balance:
            balance = float(balance)

        return balance

    def generate_wallet(self, account):
        return self.conn.getaccountaddress(account)

    def get_balance_by_account(self, account):
        return self.conn.getbalance(account)

    def get_balance_by_address(self, address):
        account = self.conn.getaccount(address)
        if account:
            return self.get_balance_by_account(account)
        return None

    def get_received_transactions_by_address(self, address=None):
        return self.conn.listreceivedbyaddress(address)

    def get_transactions_by_account(self, account=None, count=10, from_=0):
        return self.conn.listtransactions(account, count, from_)

    def validate_address(self, address):
        return self.conn.validateaddress(address)

    def unlock_wallet(self, duration_in_seconds=60):
        return self.conn.walletpassphrase(self.passphrase, duration_in_seconds)

    def lock_wallet(self):
        return self.conn.walletlock()

    def get_transaction(self, txid):
        try:
            return self.conn.gettransaction(txid)
        except Exception:
            return None
