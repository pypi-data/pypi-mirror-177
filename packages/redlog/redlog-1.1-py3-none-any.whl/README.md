# redlog

Yet another logging library in Python. This one writes logs to a Redis database and supports threads of log messages.

![Screenshot](https://raw.githubusercontent.com/lnstadrum/redlog/main/screenshot.png)

It goes with a minimalistic Python API to push logs to the database.

```python
import redlog

log = redlog.Log("localhost", 6397, db=15)
thread = log.info("Session starts")
thread.info("Client connection: socket opened")
...

```

There are fancy printing/formatting tools too.

```bash
python3 console -m redlog --db 15 --last 10m
```