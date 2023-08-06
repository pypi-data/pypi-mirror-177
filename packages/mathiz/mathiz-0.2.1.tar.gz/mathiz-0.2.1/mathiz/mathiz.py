import sys
from types import FunctionType
from threading import Thread

from wsblib import route
from wsblib import server
from wsblib import request
from wsblib import log

from http_pyparser import response


class Mathiz:
    def __init__(self) -> None:
        self._routes = []
        self._errors_callback = []
        self._process_request: request.ProcessRequest = None

    def route(self, path: str, methods: tuple = ('GET',)) -> FunctionType:
        def decorator(func):
            _route = route.Route(func, path, methods)
            self._routes.append(_route)

        return decorator

    def _process(self, client: server.Client, use_globals: bool) -> None:
        result = self._process_request.process(client, use_globals)

        if result:
            _response, _request = result
            final_response = response.make_response(_response)

            log.log_request(_response, _request)

            client.send_message(final_response)
            client.destroy()

    def run(self, host: str = '127.0.0.1', port: int = 5500, use_globals: bool = True) -> None:
        print('Mathiz Framework started')
        print(f'Creating web server in {host}:{port} address...', end=' ')

        _server = server.Server()

        try:
            _server.start(host, port)
        except OSError as err:
            print(f'\033[31mFAILED\033[m')
            if err.errno == 98:
                print(f'\n\033[31mAddress already in use.\033[m')

            sys.exit(1)
        else:
            print('\033[32mOK\033[m\n')

        self._process_request = request.ProcessRequest(
            self._routes, self._errors_callback
        )

        print('- Learn about Mathiz in https://github.com/firlast/mathiz')
        print(f'- \033[32mThe server is running at http://{host}:{port}\n\033[m')

        try:
            while True:
                client = _server.wait_client()
                th = Thread(target=self._process, args=(client, use_globals))
                th.start()
        except (KeyboardInterrupt, SystemExit, SystemError):
            print('\n\033[31mServer closed!\033[m')
            _server.destroy()
