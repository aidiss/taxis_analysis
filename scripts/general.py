import pandas as pd


def rename_columns(df):
    return df.rename(columns={
        "pickup": "pickup_time",
        "dropoff": "dropoff_time",
    })


def assign_total_fare(df):
    df.assign(total_cost=df[['fare', 'tip', 'tolls']].sum(axis=1))
    return df


def assign_trip_duration(df):
    return df.assign(trip_duration=df['dropoff']-df['pickup'])


def assign_multi_day_trip(df):
    return df.assign(
        multi_day_trip=df['dropoff'].dt.day.subtract(df['pickup'].dt.day)
    )


def preprocessing(df):
    return (
        df.rename(columns={"pickup": "pickup_time", "dropoff": "dropoff_time"})
        .assign(trip_duration=lambda x: x['dropoff'] - x['pickup'])
    )
