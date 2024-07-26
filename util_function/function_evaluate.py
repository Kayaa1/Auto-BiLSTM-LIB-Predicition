import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def rmse(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))

def rmse_percentage(y_true, y_pred):
    epsilon = 1e-10  # Small constant to avoid division by zero
    #return 100 * tf.reduce_mean(tf.abs((y_true - y_pred) / (y_true + epsilon)))
    return 100 * tf.sqrt(tf.reduce_mean(tf.square((y_true - y_pred) / y_true+ epsilon)))

def evaluate_and_save_results(y_true, predictions, file_path='evaluation_results.txt'):
    # Calculate metrics
    mae_value = mean_absolute_error(y_true, predictions)
    rmse_value = rmse(y_true, predictions)
    rmse_percent_value = rmse_percentage(y_true, predictions)
    absolute_errors = np.abs(y_true - predictions)

    # Save the results to a file
    with open(file_path, 'w') as f:
        f.write(f"MAE: {mae_value}\n")
        f.write(f"RMSE: {rmse_value}\n")
        f.write(f"RMSE Percentage: {rmse_percent_value}\n")
        f.write(f"Absolute Errors: {absolute_errors}\n")
        # Save absolute errors as a numpy file
    # Print the results
    print(f"MAE: {mae_value}")
    print(f"RMSE: {rmse_value}")
    print(f"RMSE Percentage: {rmse_percent_value}")
    #print(f"Absolute Errors: {absolute_errors}")

    # Return the results in a dictionary
    return {
        'MAE': mae_value,
        'RMSE': rmse_value,
        'RMSE Percentage': rmse_percent_value,
        'Absolute Errors': absolute_errors
    }

def plot_actual_vs_predicted_capacity(model, X_test_scaled, features, y_test, filename='Actual_vs_Predicted_Capacity.jpg'):
    """
    Generates and saves a plot comparing actual and predicted battery capacities using features['capacity'].

    Parameters:
    - model: Trained TensorFlow/Keras model used for prediction.
    - X_test_scaled: Scaled features for the test set.
    - features: DataFrame or dictionary containing 'capacity' data for all cycles.
    - y_test: Actual capacities corresponding to the test set.
    - filename: Name of the file to save the plot.
    """
    
    # Set the style of the plot to 'ggplot'
    plt.style.use('ggplot')

    # Generate predictions for the test set
    predicted_capacity = model.predict([X_test_scaled, X_test_scaled]).flatten()

    # Calculate the start of the test cycles based on the length of the test set
    total_cycles = len(features['capacity'])  # Total number of cycles in the original data
    test_cycle_start = total_cycles - len(y_test)  # Start cycle for the test data

    # Define the cycle range for the actual and predicted capacities
    test_cycles = range(test_cycle_start, total_cycles)

    # Plot the actual capacity from the original capacity data
    plt.figure(figsize=(14, 7))
    plt.plot(features['capacity'], 'o-', label='Actual Capacity', color='blue', markersize=5, linestyle='-')

    # Plot the predicted capacity for the test cycles
    plt.plot(test_cycles, predicted_capacity, 'x--', label='Predicted Capacity', color='red', markersize=5)

    # Add title and labels
    plt.title('Actual vs Predicted Capacity for Test Cycles', fontsize=16)
    plt.xlabel('Cycle', fontsize=14)
    plt.ylabel('Capacity', fontsize=14)

    # Show the legend
    plt.legend(fontsize=12)

    # Show grid lines
    plt.grid(True)

    # Save the figure as an image file
    plt.savefig(filename, bbox_inches='tight')

    # Show the plot
    plt.show()

# Example usage (assuming 'features', 'X_test_scaled', and 'y_test' are defined):
# plot_actual_vs_predicted_capacity(loaded_model, X_test_scaled, features, y_test)


def plot_actual_vs_predicted(model, X_train_scaled, X_test_scaled, features, window_size, filename='Actual_vs_Predicted_Capacity.jpg'):
    """
    Plot the actual vs. predicted capacities for both training and test data.

    Parameters:
    - model: The trained model for predicting capacities.
    - X_train_scaled: Scaled training data.
    - X_test_scaled: Scaled testing data.
    - features: A dictionary or DataFrame containing the 'capacity' data.
    - window_size: The window size used in the model for predictions.
    - filename: The filename to save the plot.
    """
    
    # Set the style of the plot to 'ggplot'
    plt.style.use('ggplot')

    # Concatenate the training and test data
    combined_data = np.concatenate((X_train_scaled, X_test_scaled), axis=0)

    # Use the model to predict capacities for the combined dataset
    predicted_capacity = model.predict([combined_data, combined_data]).flatten()

    # Calculate the total number of cycles based on the original capacity data
    total_cycles = len(features['capacity'])

    # Determine the cycle indices for the training predictions
    train_pred_indices = np.arange(window_size, window_size + len(X_train_scaled))

    # Determine the cycle indices for the test predictions
    test_pred_indices = np.arange(train_pred_indices[-1] + 1, total_cycles)

    # Plot the actual capacity (original data)
    plt.figure(figsize=(14, 7))
    plt.plot(features['capacity'], 'o-', label='Actual Capacity', color='blue', markersize=5)

    # Plot the predicted capacity for the training data with clear markers
    plt.plot(train_pred_indices, predicted_capacity[:len(X_train_scaled)], 's--', label='Predicted Capacity (Training)', color='green', markersize=5)

    # Plot the predicted capacity for the test data with clear markers
    plt.plot(test_pred_indices, predicted_capacity[len(X_train_scaled):], 'x--', label='Predicted Capacity (Testing)', color='red', markersize=5)

    # Adding title and labels with larger font sizes for readability
    plt.title('Actual vs Predicted Capacity', fontsize=16)
    plt.xlabel('Cycle', fontsize=14)
    plt.ylabel('Capacity', fontsize=14)

    # Enlarge the legend and place it in the upper right corner of the plot
    plt.legend(fontsize=12, loc='upper right')

    # Show grid lines for better readability
    plt.grid(True)

    # Save the figure as an image file
    plt.savefig(filename, bbox_inches='tight')

    # Show the plot
    plt.show()

# Example usage
# Ensure model, X_train_scaled, X_test_scaled, features, and window_size are defined before calling
# plot_actual_vs_predicted(model, X_train_scaled, X_test_scaled, features, window_size)


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preprocess_battery_data(file_path, target_column, feature_columns, window_size, test_size=0.2):
    """
    Processes battery dataset to prepare it for model training and testing, without scaling the target variable.
    
    Parameters:
    - file_path: Path to the CSV file containing the battery data.
    - target_column: The name of the target column in the dataset.
    - feature_columns: List of feature column names to be used.
    - window_size: Number of time steps to look back for prediction.
    - test_size: Proportion of the dataset to include in the test split.
    
    Returns:
    - X_train_scaled, y_train: Scaled training features and unscaled target.
    - X_test_scaled, y_test: Scaled testing features and unscaled target.
    - scaler: Fitted StandardScaler object for possible inverse transformations of features.
    """
    
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Extracting specific features
    features = data[feature_columns + [target_column]]
    
    # Creating input-output pairs
    def create_windows(features, target, window_size):
        X, y = [], []
        for i in range(len(features) - window_size):
            X.append(features[i:(i + window_size)])  # Extract a sequence of features
            y.append(target[i + window_size])       # Corresponding next value of the target
        return np.array(X), np.array(y)
    
    target_data = features[target_column].values
    feature_data = features[feature_columns].values
    
    X, y = create_windows(feature_data, target_data, window_size)
    
    # Splitting the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)
    
    # Normalization for features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
    X_test_scaled = scaler.transform(X_test.reshape(-1, X_test.shape[-1])).reshape(X_test.shape)
    
    return features,X_train_scaled, y_train, X_test_scaled, y_test, scaler




