import pandas as pd

from general import assign_multi_day_trip


def test_assign_multi_day_trip():
    df = pd.DataFrame(
        {
            "pickup": ["2019-01-01", "2019-01-01"],
            "dropoff": ["2019-01-01", "2019-01-02"],
        }, 
        dtype="datetime64[ns]"
    )
    df = assign_multi_day_trip(df)

    pd.testing.assert_series_equal(
        pd.Series([0, 1], name="multi_day_trip", dtype="int32"),
        df["multi_day_trip"],
    )
