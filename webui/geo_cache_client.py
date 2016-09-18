import requests


class GeoCacheClient(object):
    VERSION = "v1"
    def __init__(self, config):
        self.host = str(config['host'])
        self.port = str(config['port'])
        self.root = "http://{}:{}/{}".format(self.host, self.port, self.VERSION)

    def _url(self, path):
        return "{}/{}".format(self.root, path)

    def _request(self, path, data=None):
        resp = requests.get(self._url(path), data=data)

        if resp.ok:
            value = resp.json()
        else:
            value = "error: "  + str(resp.raise_for_status())
        return value

    def _post(self, path, data):
        resp = requests.post(self._url(path), json=data)

        if resp.ok:
            value = resp.json()
        else:
            value = str(resp.json())
        return value

    def status(self):
        return self._request('status')

    def query(self, postcode, radius):
        data = { "postcode" : postcode, "radius" : radius}
        value = self._post('query', data)
        return value['results'] if 'results' in value else value
