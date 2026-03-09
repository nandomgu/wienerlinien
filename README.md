## winierlinien

Retrieve real-time public transport departure information from the Wiener Linien **Monitor API**.

the functions are provided both for python and R. 

### contents

-wienerlinien.R
-wienerlinien.py
-stopids.csv

hoow to use:

1. Locate the stop ID for your desired Vienna stop

 Use the stopids.csv for reference, or seek the specific service on https://www.wienerlinien.at/fahrplaene -> pick the desired service and open the services pdf, look for your stop and  check the bottom right corner. for example, here are the stops of the U1 U-bahn https://www.wienerlinien.at/documents/11594409/11604245/fahrplan-metro-u1-oberlaa-leopoldau.pdf/af987b85-1837-b694-472b-e907b0db01ec?version=1.0&t=1760333266535

2. copy and paste the function into  your R/python
3. (optional) include an alias for your stop inside the list/dictionary of the aliases in the function. For example, "CBR2prater" is an alias for the tram stop 387 right in front of cbr.
4. call the function:
```{r}
get_wiener_times(<STOPID>, max_window=15) # services coming in the next 15 minutes
#or
get_wiener_times(stop_alias=<STOPID>, max_window=15)
```
or


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
