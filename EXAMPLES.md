Examples
------------

## Basic initialization

Import the library and create an instance of TVDBPython.

```python
import tvdbpython

client = TVDBClient("APIKEY")
```

## Anonymous usage

Some functions can be used without API key

### Retrieve time.

This retrieves the current time 

```python
time = client.get_current_time()
```