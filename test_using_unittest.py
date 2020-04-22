import signal, os, unittest
from subprocess import Popen, run, DEVNULL
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

HOST = 'http://localhost:8000'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The correct way to do this would be to use FastApi's TestClient<https://fastapi.tiangolo.com/tutorial/testing/>,  #
# but this was adaped from an earlier script<test.py> which didn't use unittest,                                    #
# and I wanted to avoid adding requests as a dependency.                                                            #
#                                                                                                                   #
#                        +-----------------------------------------------------------------------+                  #
#                        | Added, at the recommendation of Andy's, after my video call with him. |                  #
#                        +-----------------------------------------------------------------------+                  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def setUpModule():
    global pipe, resp
    pipe  = None
    running = not run(['nc', '-vz', 'localhost', '8000'], stdout=DEVNULL, stderr=DEVNULL).returncode

    # Run app, if it's not running
    while not running:
        try:
            resp = urlopen(f"{HOST}/?commodity=mango&price=53&tons=405")
            break
        except URLError as e:
            if not isinstance(e.reason, ConnectionRefusedError):
                raise
            if not pipe:
                pipe = Popen('./serve_api.sh', start_new_session=True, stdout=DEVNULL, stderr=DEVNULL)
    else:
        resp = urlopen(f"{HOST}/?commodity=mango&price=53&tons=405")


def tearDownModule():
    if pipe:
        os.killpg(pipe.pid, signal.SIGINT)
        pipe.wait()


class Test(unittest.TestCase):
    def test_happy_path(self):
        self.assertEqual(resp.status, 200)

        resp_data = resp.read()
        self.assertEqual(resp_data, b'[{"COUNTRY":"BR","TOTAL_COST":"22060.10","FIXED_OVERHEAD":"20.00","VARIABLE_COST":"54.42"},{"COUNTRY":"MX","TOTAL_COST":"21999.20","FIXED_OVERHEAD":"32.00","VARIABLE_COST":"54.24"}]')

    def test_invalid_method(self):
        with self.assertRaises(HTTPError) as cm:
            resp = urlopen(f"{HOST}/", data={})

        self.assertEqual(cm.exception.code, 405)
        resp_data = cm.exception.read()
        self.assertEqual(resp_data, b'{"detail":"Method Not Allowed"}')

    def test_missing_args(self):
        with self.assertRaises(HTTPError) as cm:
            resp = urlopen(f"{HOST}/")

        self.assertEqual(cm.exception.code, 422)
        resp_data = cm.exception.read()
        self.assertEqual(resp_data, b'{"detail":[{"loc":["query","commodity"],"msg":"field required","type":"value_error.missing"},{"loc":["query","price"],"msg":"field required","type":"value_error.missing"},{"loc":["query","tons"],"msg":"field required","type":"value_error.missing"}]}')

    def test_invalid_arg(self):
        with self.assertRaises(HTTPError) as cm:
            resp = urlopen(f"{HOST}/?commodity=mango&price=foo&tons=405")

        self.assertEqual(cm.exception.code, 422)
        resp_data = cm.exception.read()
        self.assertEqual(resp_data, b'{"detail":[{"loc":["query","price"],"msg":"value is not a valid decimal","type":"type_error.decimal"}]}')
