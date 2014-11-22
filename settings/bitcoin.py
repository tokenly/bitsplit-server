BITCOIN = {
    'user': '',
    'password': '',
    'host': '',
    'port': 8332,
    'passphrase': '',
}
BITCOIN['api_url'] = 'http://{}:{}@{}:{}/'.format(
    BITCOIN['user'],
    BITCOIN['password'],
    BITCOIN['host'],
    str(BITCOIN['port']),
)
