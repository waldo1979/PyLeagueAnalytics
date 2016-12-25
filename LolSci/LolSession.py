#!/usr/bin/python
# - Establishes request session to server
# - Enforces rate limiting
import requests
import time
from config import LolSciConfig


class LolSession:
    def __init__(self):
        lsc = LolSciConfig()
        self._rate_limit = self.set_ratelimit(lsc.requests_per_10min, lsc.requests_per_10sec)
        self._api_key = lsc.api_key
        self.region = lsc.region
        self._endpoint = self.get_endpoint(lsc.region)
        self._sess = requests.session()
        self._last_called = time.clock()

    def set_ratelimit(self, rptm, rpts):
        rate_limit1 = rptm / (60 * 10)
        rate_limit2 = rpts / 10

        if rate_limit1 < rate_limit2:
            rate_limit = rate_limit1
        else:
            rate_limit = rate_limit2

        return rate_limit

    def get_endpoint(self, region):
        endpoints = {
            'BR': 'br.api.pvp.net',
            'EUNE': 'eune.api.pvp.net',
            'EUW': 'euw.api.pvp.net',
            'JP': 'jp.api.pvp.net',
            'KR': 'kr.api.pvp.net',
            'LAN': 'lan.api.pvp.net',
            'LAS': 'las.api.pvp.net',
            'NA': 'na.api.pvp.net',
            'OCE': 'oce.api.pvp.net',
            'TR': 'tr.api.pvp.net',
            'RU': 'ru.api.pvp.net',
            'PBE': 'pbe.api.pvp.net',
            'Global': 'global.api.pvp.net'
        }

        return endpoints[region]

    def url(self, uri):
        return "https://" + self._endpoint + uri + "?api_key={0}".format(self._api_key)

    def get(self, uri):
        self.do_wait()
        url = self.url(uri)
        r = self._sess.get(url)
        return self.process_response(r)

    def post(self, uri, args=[]):
        self.do_wait()
        url = self.url(uri)
        r = self._sess.post(url, args)
        return self.process_response(r)

    def process_response(self, r):
        if r.status_code == 200:
            results = r.json()
        else:
            results = None

        self.update_wait()
        return results

    def do_wait(self):
        elapsed = time.clock() - self._last_called
        left_to_wait = self._rate_limit - elapsed
        if left_to_wait > 0:
            time.sleep(left_to_wait)

    def update_wait(self):
        self._last_called = time.clock()

if __name__ == "__main__":
    lr = LolSession()
    lr.get("/TEST")
