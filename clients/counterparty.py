import json
import requests
from requests.auth import HTTPBasicAuth


class Counterparty(object):
    def __init__(self, api_url, user, password, miner_fee, dust_size):
        self.api_url = api_url
        self.user = user
        self.password = password
        self.miner_fee = miner_fee
        self.dust_size = dust_size

    def get_balances(self):
        return self._post(method='get_balances')

    def get_balance_by_address(self, address, asset):
        results = self._post(method='get_balances', params={
            'filters': {'field': 'address', 'op': '==', 'value': address}
        })
        for result in results:
            if result["asset"] == asset:
                return result["quantity"]
        return 0

    def create_send(self, params):
        return self._post(method='create_send', params=params)

    def broadcast_transaction(self, signed_tx_hex):
        return self._post(method='broadcast_tx', params={
            'signed_tx_hex': signed_tx_hex
        })

    def sign_transaction(self, unsigned_tx_hex):
        return self._post(method='sign_tx', params={
            'unsigned_tx_hex': unsigned_tx_hex
        })

    def get_asset(self, asset):
        """ Alias for self.get_asset_info """
        return self.get_asset_info(asset)

    def get_asset_info(self, asset):
        result = self._post(method="get_asset_info", params={
            "assets": [asset]
        })
        if not result or len(result) == 0:
            return None
        return result[0]

    def _post(self, method, params=None):
        headers = {'content-type': 'application/json'}
        auth = HTTPBasicAuth(self.user, self.password)

        raw_payload = {
            "method": method,
            "jsonrpc": "2.0",
            "id": 0,
        }

        if params:
            raw_payload["params"] = params

        payload = json.dumps(raw_payload)        
        response = requests.post(
            self.api_url,
            data=payload,
            headers=headers,
            auth=auth)
       # raise Exception(response.text)
        try:
            return json.loads(response.text)["result"]
        except Exception:
            raise Exception(response.text)
