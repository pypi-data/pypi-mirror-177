import requests
from typing import Optional


class MyTelegramBot:
    def __init__(self, token):
        self.token = token
        self._message_handlers = []
        self.last_update_id = 0
        self.GET_UPDATE_TIMEOUT = 10

    def message_handler(self, command: Optional[str] = None):
        def decorator(handler):
            handler_dict = {'function': handler, 'command': command}

            self._message_handlers.append(handler_dict)
            return handler

        return decorator

    def start(self):
        while True:
            try:
                updates = self.get_updates()
                self.process_updates(updates)

            except Exception as err:
                print(f"\n{err=}, {type(err)=}")

    def get_updates(self):
        request_name = r'getUpdates'
        params = {
            'offset': self.last_update_id + 1,
            'timeout': self.GET_UPDATE_TIMEOUT,
        }

        return self._make_request(request_name, params=params)

    def _make_request(self, request_name, method='get', params=None):
        if not self.token:
            raise Exception("Token is not defined")

        request_url = "https://api.telegram.org/bot{0}/{1}".format(
            self.token, request_name
        )

        connect_timeout = 15
        read_timeout = 25
        if 'timeout' in params and params['timeout']:
            connect_timeout = params['timeout']
            read_timeout = connect_timeout + 10

        response = requests.sessions.Session().request(
            method,
            request_url,
            params=params,
            timeout=(connect_timeout, read_timeout),
        )

        json_res = self._check_response(response)
        return json_res['result']

    @staticmethod
    def _check_response(response):
        try:
            response_json = response.json()
        except Exception:
            raise Exception("The server returned an invalid JSON response")
        if response.status_code != 200:
            raise Exception("Response status code is not 200")
        if not response_json['ok']:
            raise Exception("Response status is not OK")
        return response_json

    def process_updates(self, updates):
        if not updates:
            return

        new_messages = []
        for update in updates:
            if update['update_id'] > self.last_update_id:
                self.last_update_id = update['update_id']
            if 'message' in update and update['message']:
                new_messages.append(update['message'])

        if new_messages:
            self.process_new_messages(new_messages)

    def process_new_messages(self, messages):
        for message in messages:
            command, text = self._get_command(message['text'])
            message['text'] = text
            for handler in self._message_handlers:
                if command == handler['command']:
                    handler['function'](message)
                    return

    @staticmethod
    def _get_command(message_text) -> tuple:
        command = None
        text = message_text
        if message_text.startswith('/'):
            if ' ' in message_text:
                command, text = message_text.split(' ', 1)
            else:
                command, text = message_text, None
            command = command[1:]
        return command, text

    def send_message(self, chat_id, text):
        request_name = r'sendMessage'
        params = {
            'chat_id': chat_id,
            'text': text,
        }
        response = self._make_request(
            request_name, params=params, method='post'
        )

        return response
