## winierlinien

Retrieve real-time public transport departure information from the Wiener Linien **Monitor API**.

the functions are provided both for python and R. 

### contents

-wienerlinien.R
-wienerlinien.py
-stopids.csv
-tram_times.py (executable python code fromm shell)
-run_tram_monitor.sh (shell script that loops through the python script every few seconds)

how to use:

1. Locate the stop ID for your desired Vienna stop

Method a) Use the stopids.csv for reference, find the name of your stop, and confirm with the GPS coordinates. 
 
 Method b) seek the specific service on https://www.wienerlinien.at/fahrplaene -> pick the desired service and open the services pdf, look for your stop and look for "Haltestelle" in the bottom right corner. For example, here are the stops of the U6 U-bahn [https://www.wienerlinien.at/documents/11594409/29526878/fahrplan-metro-u6--schulplan-kein-halt-in-der-station-tscherttegasse-in-fahrtrichtung-siebenhirten-wegen-bahnsteigsanierung-ausnahme-mo-do-von-22-uhr-bis-betriebsschluss-siebenhirten-floridsdorf.pdf/f6516287-df25-fec8-b82c-0f10446739c5?version=1.1&t=1769595795494]

2. copy and paste the function into  your R/python
   
3. (optional) include an alias for your stop inside the list/dictionary of the aliases in the function. For example, "CBR2prater" is an alias for the tram stop 387 right in front of cbr.
   
4a. To run from a python or R session, call the function:
```{r}
get_wiener_times(<STOPID>, max_window=15) # services coming in the next 15 minutes
#or if you added an alias or know it
get_wiener_times(stop_alias=<STOP ALIAS>, max_window=15)
```
4b. alternatively, run the function in a loop and update tramtimes.csv every few seconds:

First, make the shell script executable
```{bash}
chmod -x run_tram_monitor.sh
```
Second, enter this to run the script in the background:

```{bash}
nohup ./run_tram_monitor.sh > tram_monitor.log 2>&1 &
```
Once the above is executing, you can look at at the table from the command line doing

```{bash}
column -s -t tramtimes.csv
```

or simply show the times in plain .csv format

```{bash}
cat tramtimes.csv
```

### further details about the functions.


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
```

