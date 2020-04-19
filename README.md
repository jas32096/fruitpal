# Fruitpal

Docs at `/docs` and `/redoc`

---

`./serve_api.sh` to run.

`python3 test.py` run tests.

Both commands will setup your environment for you, if needed. 

---

```http
GET /?commodity=mango&price=53&tons=405 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8000
User-Agent: HTTPie/2.0.0



HTTP/1.1 200 OK
content-length: 181
content-type: application/json
date: Sun, 19 Apr 2020 02:31:59 GMT
server: uvicorn

[
    {
        "COUNTRY": "BR",
        "FIXED_OVERHEAD": "20.00",
        "TOTAL_COST": "22060.10",
        "VARIABLE_COST": "54.42"
    },
    {
        "COUNTRY": "MX",
        "FIXED_OVERHEAD": "32.00",
        "TOTAL_COST": "21999.20",
        "VARIABLE_COST": "54.24"
    }
]
```
