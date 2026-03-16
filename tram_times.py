import os
import requests
import pandas as pd


def get_wiener_times(stop_id=None, stop_alias=None, max_window=15):

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

    # normalize inputs to lists
    if stop_alias is not None:
        if isinstance(stop_alias, str):
            stop_alias = [stop_alias]

        stop_ids = [stop_ref[a] for a in stop_alias]

    elif stop_id is not None:
        if isinstance(stop_id, int):
            stop_id = [stop_id]

        stop_ids = stop_id
        stop_alias = [None] * len(stop_ids)

    else:
        raise ValueError("Either stop_id or stop_alias must be provided")

    base_url = "https://www.wienerlinien.at/ogd_realtime/monitor"

    all_results = []

    for sid, alias in zip(stop_ids, stop_alias):

        r = requests.get(base_url, params={"stopId": sid})
        r.raise_for_status()

        data = r.json()
        monitors = data.get("data", {}).get("monitors", [])

        for monitor in monitors:
            for line in monitor.get("lines", []):
                departures = line.get("departures", {}).get("departure", [])

                for dep in departures:
                    all_results.append({
                        "stop.id": sid,
                        "stop.alias": alias,
                        "line": line.get("name"),
                        "dest": line.get("towards"),
                        "when": dep.get("departureTime", {}).get("timePlanned"),
                        "countdown": dep.get("departureTime", {}).get("countdown")
                    })

    df = pd.DataFrame(all_results)

    if not df.empty:
        df = df[df["countdown"] < max_window]

    return df


if __name__ == "__main__":

    df = get_wiener_times(stop_alias=["CBR2prater", "CBR2westbhf"], max_window=15)

    # public path for user
    output_path = os.path.expanduser("~/tramtimes.csv")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)
