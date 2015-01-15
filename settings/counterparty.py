COUNTERPARTY = {
    'user': '',
    'password': '',
    'ip': 'localhost:4000',
    #'prefix': 'XCP_',
    #'satoshi_mod': 100000000,
    'base_fee': 5000,  # satoshis
    'dust_size': 2500
}
#COUNTERPARTY['api_url'] = 'http://' + COUNTERPARTY['user'] + ':' + COUNTERPARTY['password'] + '@' + COUNTERPARTY['ip'] + '/api/'
COUNTERPARTY['api_url'] = 'http://' + COUNTERPARTY['ip'] + '/api/'
