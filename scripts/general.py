import pandas as pd
from matplotlib import colors
import requests


def rename_columns(df):
    return df.rename(columns={
        "pickup": "pickup_time",
        "dropoff": "dropoff_time",
    })


def assign_total_fare(df):
    return df.assign(total_cost=df[['fare', 'tip', 'tolls']].sum(axis=1))


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


def split_datetime_to_cols(df, column: str):
    df[f'{column}_year'] = df[column].dt.year
    df[f'{column}_month'] = df[column].dt.month
    df[f'{column}_day'] = df[column].dt.day
    return df


def is_multi_year(df):
    # Was trip a multi year trip?
    df.assign(is_multi_year=df['dropoff'].dt.year - df['pickup'].dt.year)


def combine_pickup_zone_and_borough(df):
    # Combining pickup zone and borough?
    pickup_zone_borough = df['pickup_zone'] + '_' + df['pickup_borough']
    return df.assign(pickup_zone_borough=pickup_zone_borough)


def most_tipped_color(df):
    # What colors were tipped the most?
    return df.groupby('color')['tip'].sum()


def extract_time_of_day(df):
    # Extract PM and AM from pickup_datetime.
    # Might return capital or small letters.
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    return df.assign(time_of_day=df['pickup'].dt.strftime('%p'))


def duration_by_time_of_day(df):
    # # What duration of trip was PM and AM?
    return df.groupby('time_of_day')['duration'].mean()


def duration_by_time_of_day_and_borough(df):
    # # What duration of trip was PM and AM for each borough?
    return df.groupby(['time_of_day', 'borough'])['duration'].mean()


def tip_by_pickup(df):
    # # What was the average tip for each zone?
    return df.groupby('pickup_zone')['tip'].mean()


def duration_by_time_of_day_and_borough_and_zone(df):
    # # What was the average tip for each borough and zone?
    return df.groupby('pickup_zone_borough')['tip'].mean()


def set_categorical(df):
    return df.assign(payment=df['payment'].astype('category'))


def correlation_between_payment_and_color(df):
    # Is there correlation between payment and color.
    return df[['color', 'payment']].corr()


def average_tip_by_payment(df):
    # What is the average tip for each payment type?
    return df.groupby('payment')['tip'].mean()


def average_tip_by_payment_and_color(df):
    # What is the average tip for each payment type and color?
    return df.groupby(['payment', 'color'])['tip'].mean()


def split_payment_to_groups(df):
    return df.assign(
        tip_group=pd.qcut(
            df['tip'],
            q=4,
            labels=['low', 'medium', 'high'],
            duplicates='drop'
        )
    )


def get_weather(latitude, longitude, start_date, end_date):
    hourly = [
        'temperature_2m', 'relativehumidity_2m', 'dewpoint_2m', 'apparent_temperature', 'pressure_msl', 'surface_pressure', 'precipitation', 'rain', 'snowfall', 'weathercode', 'cloudcover', 'cloudcover_low', 'cloudcover_mid', 'cloudcover_high', 'shortwave_radiation', 'direct_radiation', 'diffuse_radiation', 'direct_normal_irradiance', 'windspeed_10m', 'windgusts_10m'
    ]
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': start_date,
        'end_date': end_date,
        'hourly': ','.join(hourly)
    }
    url = 'https://archive-api.open-meteo.com/v1/archive'
    data = requests.get(url, params=params).json()
    return data


def color_codes(df):
    df['color'].apply(
        lambda x: pd.Series(data=colors.to_rgb(x))
    ).rename(columns={0: 'red', 1: 'green', 2: 'blue'})


def color_codes_efficient(df):
    color_string_to_rgb = pd.concat({
        color: pd.Series(colors.to_rgb(color))
        for color in df['color'].unique()
    }).unstack()
    return pd.merge(
        df['color'], color_string_to_rgb, left_on='color', right_index=True
    )


def preprocessingv2(df):
    # Rename columns
    # Choose data types
    # Deal with duplicates
    # Deal with outliers
    # Deal with missing values
    # Enrich data with new columns
    # Enrich data with external data
    # Rename columns
    ...


# May functions for specific columns
# pickip, dropoff, duration (datetimes)
# fare, tip, tolls, total_cost (prices)
# pickup_location, dropoff_location (locations)
# passenger count
# payment type
# color


def deal_with_missing_values(df):
    return df
