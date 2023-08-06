import requests
from requests import RequestException

from . import models


class TelegramClient:
    def __init__(self, tocken):
        self.tocken = tocken
        self.server_url = "https://api.telegram.org/bot"
        self.user_api_url = self.server_url + tocken

    def get_updates(self, offset=None):
        route = "/getUpdates"
        url = self.user_api_url + route
        if offset is not None:
            url += f"?offset={offset}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = models.ResponseUpdate.parse_raw(response.text)
            if data.ok:
                return data.result
            else:
                raise RuntimeError
        except RequestException:
            return None
        except ValueError:
            return None
        except RuntimeError:
            return None

    def set_updates_readed(self, offset):
        response = self.get_updates(offset + 1)
        if response is None:
            return False
        else:
            return True

    def sent_message(self, id, text, parse_mode=None):
        route = "/sendMessage"
        params = f"?chat_id={id}&text={text}"
        if parse_mode is not None:
            params += f"&parse_mode={parse_mode}"
        url = self.user_api_url + route + params
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = models.ResponseMassage.parse_raw(response.text)

            if data.result.text == text:
                return True
            else:
                return False
        except RequestException:
            return False
        except ValueError:
            return False
        except RuntimeError:
            return False
