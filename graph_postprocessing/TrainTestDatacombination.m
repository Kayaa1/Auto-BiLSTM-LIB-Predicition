function combined_data = TrainTestDatacombination(train_data, test_data, window_size)
    % Check if window_size is provided, if not assign default value
    if nargin < 3
        window_size = 5;
    end
    
    % Create an array of NaN values to pad the start of the data
    padding = NaN(1, window_size);
    
    % Concatenate the NaN padding, training data, and testing data
    combined_data = [padding, train_data, test_data];
end
