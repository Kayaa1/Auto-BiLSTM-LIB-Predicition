%% load the data
load("datafrommatlab(frompython).mat")
%%  Box Plot

combined_data = [absolute_errors_B0005_Bilstm,
                 absolute_errors_B0005_CNN,
                 absolute_errors_B0005_CNN_Bilstm_parallel,
                 absolute_errors_B0005_CNN_Bilstm_sequential];
combined_data = transpose(combined_data);
% Labels for each group in the boxplot
group_labels = {'BiLSTM', 'CNN', 'CNN BiLSTM par', 'CNN_BiLSTM seq'};

% Verify that the number of labels matches the number of columns in combined_data
assert(size(combined_data, 2) == length(group_labels), 'Number of labels must match number of columns');

% Create the box plot
figure;
boxplot(combined_data, 'Labels', group_labels);
title('Distribution of Absolute Errors for Different Models');
ylabel('Absolute Error');

%% Compare the result of different model

% Use TrainTestDatacombination function to prepare data for plotting
combined_CNN = TrainTestDatacombination(CNN_predictions_train, CNN_predictions);
combined_Bilstm = TrainTestDatacombination(Bilstm_predictions_train, Bilstm_predictions);
combined_CNN_Bilstm_P =TrainTestDatacombination(CNN_Bilstm_parallel_predictions_train, CNN_Bilstm_parallel_predictions);
combined_CNN_Bilstm_S =TrainTestDatacombination(CNN_Bilstm_sequential_predictions_train, CNN_Bilstm_sequential_predictions);

% Create a new figure for plotting
figure;

% Plot the actual capacity with high contrast
plot(B0005_capacity, 'LineWidth', 2, 'Color', 'black', 'DisplayName', 'Actual Capacity');
hold on;
% Plot the smoothed capacity with high contrast
% plot(smoothed_B0005_capacity, 'LineWidth', 2, 'Color', [1, 0.55, 0], 'DisplayName', 'Smoothed Capacity');

% Plot the model predictions with lower contrast using dashed lines
plot(combined_CNN, '--', 'Color', 'green', 'LineWidth', 1.5, 'DisplayName', 'CNN Predicted Capacity');
plot(combined_Bilstm, '--', 'Color', 'red', 'LineWidth', 1.5, 'DisplayName', 'BiLSTM Predicted Capacity');
plot(combined_CNN_Bilstm_P, '--','Color', 'cyan', 'LineWidth', 1.5, 'DisplayName', 'CNN-BiLSTM Parallel Predicted Capacity');
plot(combined_CNN_Bilstm_S, '--', 'Color', 'blue', 'LineWidth', 1.5, 'DisplayName', 'CNN-BiLSTM Sequential Predicted Capacity');

% Add the testing set start line without including it in the legend
xl = xline(window_size + length(CNN_predictions_train), '--k', 'Testing Set Start', 'LabelHorizontalAlignment', 'left', 'LineWidth', 1.5);
set(get(get(xl,'Annotation'),'LegendInformation'),'IconDisplayStyle','off');

% Add title, labels, and legend
title('Different Models Prediction for B0005');
xlabel('Cycles');
ylabel('Capacity (Ah)');
legend('show','Location', 'Best');

% Show grid for better readability
grid on;


