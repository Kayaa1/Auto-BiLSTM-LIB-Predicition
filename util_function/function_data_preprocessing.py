# Function to create input-output pairs for time-series prediction using a sliding window approach
import pandas as pd
import numpy as np

def create_windows(features, target, window_size):
    """
    Generates sequences of features (X) and corresponding next values (y) from time-series data.
    """
    X, y = [], []
    for i in range(len(features) - window_size):
        X.append(features[i:(i + window_size)])  # Extract a sequence of features
        y.append(target[i + window_size])       # Corresponding next value of the target
    return np.array(X), np.array(y)

def custom_moving_average(data, filter_window_size):
    """Compute the moving average of a 1D array, using a custom scheme for the first elements.

    Args:
    - data (array-like): The 1D array of data points.
    - filter_window_size (int): The number of data points to consider for each average.

    Returns:
    - array-like: The array of moving averages, same length as 'data'.
    """
    # Initialize an array to hold the moving averages.
    smoothed_data = np.zeros(len(data))
    
    # Apply custom averaging for the first few elements based on the available data
    for i in range(filter_window_size):
        if i == 0:
            smoothed_data[i] = data[i]
        else:
            custom_weights = np.array([1/(j+1) for j in range(i, -1, -1)])
            smoothed_data[i] = np.dot(data[:i+1], custom_weights) / custom_weights.sum()

    # Calculate the moving average for the rest of the data points.
    for i in range(filter_window_size, len(data)):
        smoothed_data[i] = np.mean(data[i - filter_window_size + 1:i + 1])

    return smoothed_data