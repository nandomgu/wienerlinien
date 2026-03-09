import requests
import pandas as pd


def get_wiener_times(stop_id=None, stop_alias=None, max_window=15):
    # alias mapping
    stop_ref = {
        "CBR2prater": 381,
        "CBR2westbhf": 355,
        "home2westbhf": 1561,
        "home2rodaun": 1533,
        "westbhf2CBR": 370,
        "westbhfU6flor": 4619,
        "westbhfU6sieb": 4610,
        "alserU6sieb": 4606,
        "gumpU6flor": 4618,
        "gumpU6sieb": 4611,
    }

    if stop_alias is not None:
        stop_id = stop_ref.get(stop_alias)

    if stop_id is None:
        raise ValueError("Either stop_id or stop_alias must be provided")

    base_url = "https://www.wienerlinien.at/ogd_realtime/monitor"

    r = requests.get(base_url, params={"stopId": stop_id})
    r.raise_for_status()

    data = r.json()

    monitors = data.get("data", {}).get("monitors", [])
    if not monitors:
        return "No real-time departures found."

    results = []

    for monitor in monitors:
        for line in monitor.get("lines", []):
            departures = line.get("departures", {}).get("departure", [])

            for dep in departures:
                results.append({
                    "stop.id": stop_id,
                    "stop.alias": stop_alias,
                    "line": line.get("name"),
                    "dest": line.get("towards"),
                    "when": dep.get("departureTime", {}).get("timePlanned"),
                    "countdown": dep.get("departureTime", {}).get("countdown")
                })

    if not results:
        return "No real-time departures found."

    df = pd.DataFrame(results)

    # filter by max_window like dplyr::filter(countdown < max.window)
    df = df[df["countdown"] < max_window]

    return df
