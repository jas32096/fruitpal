import signal, os
from subprocess import Popen, run, DEVNULL
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

HOST = 'http://localhost:8000'

if __name__ == '__main__':
    pipe = None
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
                pipe = Popen('./serve_api.sh', start_new_session=True)
    else:
        resp = urlopen(f"{HOST}/?commodity=mango&price=53&tons=405")
    
    # Happy path
    assert resp.status == 200

    resp_data = resp.read()
    assert resp_data == b'[{"COUNTRY":"BR","TOTAL_COST":"22060.10","FIXED_OVERHEAD":"20.00","VARIABLE_COST":"54.42"},{"COUNTRY":"MX","TOTAL_COST":"21999.20","FIXED_OVERHEAD":"32.00","VARIABLE_COST":"54.24"}]'

    # Invalid method
    try:
        resp = urlopen(f"{HOST}/", data={})
    except HTTPError as err:
        assert err.code == 405
        resp_data = err.read()
        assert resp_data == b'{"detail":"Method Not Allowed"}'
    else:
        assert False

    # Missing args
    try:
        resp = urlopen(f"{HOST}/")
    except HTTPError as err:
        assert err.code == 422
        resp_data = err.read()
        assert resp_data == b'{"detail":[{"loc":["query","commodity"],"msg":"field required","type":"value_error.missing"},{"loc":["query","price"],"msg":"field required","type":"value_error.missing"},{"loc":["query","tons"],"msg":"field required","type":"value_error.missing"}]}'
    else:
        assert False

    # Invalid arg
    try:
        resp = urlopen(f"{HOST}/?commodity=mango&price=foo&tons=405")
    except HTTPError as err:
        assert err.code == 422
        resp_data = err.read()
        assert resp_data == b'{"detail":[{"loc":["query","price"],"msg":"value is not a valid decimal","type":"type_error.decimal"}]}'
    else:
        assert False

    if pipe:
        os.killpg(pipe.pid, signal.SIGINT)
        pipe.wait()