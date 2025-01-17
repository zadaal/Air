import pandas as pd

def moving_average_threshold(df, timeWindow, city, id, param, threshold):
    # Filter the dataframe to include only the specified city, id, and param
    df_filtered = df[(df['City'] == city) & (df['Id'] == id) & (df['param'] == param)]

    # Convert the 'Timestamp' column to a datetime object
    df_filtered['Timestamp'] = pd.to_datetime(df_filtered['Timestamp'])

    # Sort the dataframe by timestamp
    df_filtered = df_filtered.sort_values('Timestamp')

    # Define a rolling window for the specified time period
    window = pd.Timedelta(seconds=timeWindow)

    # Compute the rolling mean
    rolling_mean = df_filtered.set_index('Timestamp').rolling(window).mean()

    # Filter the rolling mean to include only the timestamps where the mean is above the threshold
    threshold_mask = rolling_mean['value'] > threshold
    rolling_mean_above_threshold = rolling_mean[threshold_mask]

    # Extract the timestamps and values where the rolling mean is above the threshold
    timestamps = rolling_mean_above_threshold.index.strftime('%Y-%m-%d %H:%M:%S')
    values = rolling_mean_above_threshold['value'].tolist()

    return timestamps, values
