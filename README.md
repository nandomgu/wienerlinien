## winierlinien

Retrieve real-time public transport departure information from the Wiener Linien **Monitor API**.

the functions are provided both for python and R. 

### contents

wienerlinien.R
wienerlinien.py
stopids.csv
## `get_wiener_times()`

This function queries the Wiener Linien Open Government Data (OGD) realtime endpoint and returns upcoming departures for a given stop. Results are returned as a structured dataframe filtered to only include departures occurring within a specified time window.

### Features

- Accesses the **Wiener Linien realtime monitor API**
- Supports stop lookup via:
  - `stop_id` (numeric Wiener Linien stop ID)
  - `stop_alias` (custom shortcut defined in the function)
- Extracts and formats:
  - line name
  - destination
  - planned departure time
  - countdown (minutes until departure)
- Filters results to departures within a configurable time window

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `stop_id` | `int` | Wiener Linien stop ID |
| `stop_alias` | `str` | Optional alias mapped to a predefined stop ID |
| `max_window` | `int` | Maximum number of minutes until departure to include (default: `15`) |

If `stop_alias` is provided, it overrides `stop_id` using a predefined mapping of frequently used stops.

### Returns

A **pandas DataFrame** containing upcoming departures:

| column | description |
|------|-------------|
| `stop.id` | Stop ID used in the query |
| `stop.alias` | Alias used for the stop (if any) |
| `line` | Transit line name |
| `dest` | Destination of the vehicle |
| `when` | Planned departure timestamp |
| `countdown` | Minutes until departure |

If no departures are found, the function returns a message indicating that no realtime data is available.

### Example

```python
df = get_wiener_times(stop_alias="westbhfU6flor", max_window=10)
print(df)
