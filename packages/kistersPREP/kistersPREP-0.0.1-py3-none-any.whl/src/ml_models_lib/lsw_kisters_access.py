import pandas as pd
import requests

_KISTERS_URL = "https://www.dp.l-sw.dev/api/kisters-integration-service/tenant/{}/timeseries/{}/values?from={}&to={}"


def get_timeseries(timeseries_id, tenant, timerange_start, timerange_end):
    url = _KISTERS_URL.format(tenant, timeseries_id, timerange_start, timerange_end)

    # request is a list of dictionaries, i.e. timeseries ts is key to value v of last measurement {'ts': xxx, 'v': yyy}
    request = requests.get(url=url).json()
    df = pd.DataFrame.from_dict(request, orient="columns")

    df["Timestamp"] = _convert_tz_from_utc_to_berlin(df)
    df["Timestamp"] = _slice_off_tz(df)
    return df[["Timestamp", "v"]]


def _convert_tz_from_utc_to_berlin(df):
    return pd.to_datetime(df["ts"]).dt.tz_convert(tz="Europe/Berlin").astype(str)


def _slice_off_tz(df):
    return [x[:-6] for x in df["Timestamp"]]


def put_results_into_kisters(data):
    headers = {"Content-Type": "application/json"}
    requests.put(
        'http://www.dp.l-sw.dev/api/kisters-integration-service/tenant/PROGNOSESTROM/timeseries/31329192/values',
        data=data, headers=headers)
