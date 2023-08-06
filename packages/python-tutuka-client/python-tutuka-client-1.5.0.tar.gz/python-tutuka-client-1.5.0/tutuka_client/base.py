from datetime import datetime
from xmlrpc import client as xmlrpc_client

import requests

from tutuka_client.errors import GenericError, TutukaException
from tutuka_client.response_codes import (
    ERROR_RESPONSE_CODES_EXCEPTIONS,
    SUCCESS_RESPONSE_CODES,
)
from tutuka_client.utils import checksum_normalize, date_time_normalize, hmac_with_sha1


def dumps(method_name: str, arguments: list):
    return xmlrpc_client.dumps(
        tuple(arguments),
        method_name,
    )


def loads(response: str):
    if not _is_xml(response):
        raise GenericError(response.strip())

    return xmlrpc_client.loads(
        response,
        use_builtin_types=True,
    )


def _is_xml(response: str):
    return response.startswith('<?xml')


class BaseClient(object):
    def __init__(self, terminal_id, password, host, path, http_client=requests):
        self.terminal_id = terminal_id
        self.password = password
        self.host = host
        self.path = path
        self.session = http_client.Session()
        self.session.headers.update({'Content-Type': 'application/xml'})

    def generate_checksum(self, method_name: str, arguments: list = None):
        if arguments is None:
            arguments = []

        concat = ''.join([checksum_normalize(argument or '') for argument in arguments])
        string_to_sign = method_name + concat

        return hmac_with_sha1(
            self.password.encode('utf-8'),
            string_to_sign.encode('utf-8'),
        )

    def execute(self, method_name: str, arguments: list):  # noqa: WPS210
        arguments.append(datetime.now())
        checksum = self.generate_checksum(method_name, arguments)
        arguments.append(checksum)

        body = dumps(method_name, arguments)
        response = self.session.post(
            '{host}{path}'.format(host=self.host, path=self.path), data=body,
        )
        loads_result = loads(response.text)[0][0]

        if 'resultCode' not in loads_result:
            raise TutukaException('no result code')
        result_code = loads_result['resultCode']

        if result_code not in SUCCESS_RESPONSE_CODES.values():
            result_text = loads_result.get('resultText', '')
            error = ERROR_RESPONSE_CODES_EXCEPTIONS.get(str(result_code), GenericError)
            raise error(result_text, result_code)

        return {
            key: date_time_normalize(value)
            for (key, value) in loads_result.items()  # noqa: WPS110
        }
