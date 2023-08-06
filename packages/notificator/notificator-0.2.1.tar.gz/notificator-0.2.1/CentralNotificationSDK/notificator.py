from typing import Optional

import requests


class Notificator:
    def __init__(self, name, token, host=None):
        self.host = host or 'https://notice.6-79.cn'
        if self.host.endswith('/'):
            self.host = self.host[:-1]

        self.name = name
        self.token = token

    def _send(self, data: dict, channel: str):
        del data['self']

        with requests.post(
            url=f'{self.host}/api/channel/{channel}',
            json=data,
            headers=dict(
                Auth=f'{self.name}${self.token}',
            )
        ) as resp:
            # print(resp.content)
            return resp.json()

    def bark(
            self,
            uri: str,
            content: str,
            title: Optional[str] = None,
            sound: Optional[str] = None,
            icon: Optional[str] = None,
            group: Optional[str] = None,
            url: Optional[str] = None,
    ):
        return self._send(data=locals(), channel='bark')

    def sms(
            self,
            phone: str,
            content: str,
    ):
        return self._send(data=locals(), channel='sms')

    def mail(
            self,
            mail: str,
            content: str,
            subject: Optional[str] = None,
            appellation: Optional[str] = None,
    ):
        return self._send(locals(), channel='mail')
