load('capacity_data.mat')
%% Using fft to distingulish the frequency
fs = 1; %sampling  fs = 1 ,per cycle
L = length(capacity_B0005);  %length 167
Y_fft=fft(capacity_B0005);  % length 167
P2 = abs(Y_fft/L); 
P1 = P2(1:L/2+1); 
P1(2:end-1) = 2*P1(2:end-1);
f = fs*(-L/2:L/2-1)/L; % per 1 Hz
figure;
stem(f,fftshift(P2)) % Shifts the zero to the center
title('Double-Sided Amplitude Spectrum of B0005')
xlabel('Frequency $(\frac{1}{167}$ Hz)', 'Interpreter', 'latex');
ylabel('|P(f)|')
%% Choice cut-off frequenices
% power_5 = sum(P2); %2.5594
% sum(P2(1:30)) %1.96611
scaling_number = 175;
scaling_factor = scaling_number/length(capacity_B0005);
LPF_Window = 16;
% Using Ideal LPF filter to filter to smooth high frequency componment
LPF_capacity_B0005 = fftshift(Y_fft);
LPF_capacity_B0005 =ifft(LPF_capacity_B0005(L/2-LPF_Window :L/2+LPF_Window),scaling_number);  % once choosing the cut_off frequency,using rectangular window to padding 0
%178 is the scalleing factor
figure;
Modified_LPF_capacity_B0005 = LPF_capacity_B0005 * scaling_factor;
plot(abs(Modified_LPF_capacity_B0005))
hold on;
plot(capacity_B0005)
legend('Capacity after using LPF with interpolation','Raw Capacity')
title('Comparing of Filtering and raw data of B0005')
xlabel('Cycles');
ylabel("Capacity(Ah)")
%%
% endpoint = 168;
% startpoint =  endpoint-length(capacity_B0005) +1;
startpoint = 6;
endpoint = length(capacity_B0005) + startpoint -1;
% Where 6:173 are the intersection points and ensure the points are cycle
%number

figure;
FinalModified_LPF_capacity_B0005 =Modified_LPF_capacity_B0005(startpoint:endpoint);
plot(abs(FinalModified_LPF_capacity_B0005),'blue')
hold on;
plot(capacity_B0005,'red')
legend('Final filtering Capacity','Raw Capacity')
title('Comparing of Final Filtering and raw data of B0005')
xlabel('Cycles');
ylabel("Capacity(Ah)")
rmse_B0005 = sqrt(sum(((capacity_B0005-abs(FinalModified_LPF_capacity_B0005)).^2)));
RMSE_per_B0005 = 100 * sqrt(mean((capacity_B0005 - FinalModified_LPF_capacity_B0005).^2)) / mean(capacity_B0005);
MAE_per_B0005 = 100 * mean(abs(capacity_B0005 - FinalModified_LPF_capacity_B0005)) / mean(capacity_B0005);
display(rmse_B0005)
%% Do the same thing of B0006
fs = 1; %sampling  fs = 1 ,per cycle
L = length(capacity_B0006);  %length 167
Y_fft=fft(capacity_B0006);  % length 167
P2 = abs(Y_fft/L); 
P1 = P2(1:L/2+1); 
P1(2:end-1) = 2*P1(2:end-1);
f = fs*(-L/2:L/2-1)/L; % per 1 Hz
figure;
stem(f,fftshift(P2)) % Shifts the zero to the center
title('Double-Sided Amplitude Spectrum of B0006')
xlabel('Frequency $(\frac{1}{167}$ Hz)', 'Interpreter', 'latex');
ylabel('|P(f)|')
%% Choice cut-off frequenices

scaling_number = 176;
scaling_factor = scaling_number/length(capacity_B0006);
LPF_Window = 22;
% Using Ideal LPF filter to filter to smooth high frequency componment
LPF_capacity_B0006 = fftshift(Y_fft);
LPF_capacity_B0006 =ifft(LPF_capacity_B0006(L/2-LPF_Window :L/2+LPF_Window),scaling_number);  % once choosing the cut_off frequency,using rectangular window to padding 0
%178 is the scalleing factor
figure;
Modified_LPF_capacity_B0006 = LPF_capacity_B0006 * scaling_factor;
plot(abs(Modified_LPF_capacity_B0006))
hold on;
plot(capacity_B0006)
legend('Capacity after using LPF with Padding','Raw Capacity')
title('Comparing of Filtering and raw data of B0006')
xlabel('Cycles');
ylabel("Capacity(Ah)")
%% plot the final filter output

startpoint = 5;
endpoint = length(capacity_B0006) + startpoint -1;

figure;
FinalModified_LPF_capacity_B0006 =Modified_LPF_capacity_B0006(startpoint:endpoint);
plot(abs(FinalModified_LPF_capacity_B0006),'blue')
hold on;
plot(capacity_B0006,'red')
legend('Final filtering Capacity','Raw Capacity')
title('Comparing of Final Filtering and raw data of B0006')
xlabel('Cycles');
ylabel("Capacity(Ah)")
rmse_B0006 = sqrt(sum(((capacity_B0006-abs(FinalModified_LPF_capacity_B0006)).^2)));
display(rmse_B0006)

 %%  Do the same thing of B0007
fs = 1; %sampling  fs = 1 ,per cycle
L = length(capacity_B0007);  %length 167
Y_fft=fft(capacity_B0007);  % length 167
P2 = abs(Y_fft/L); 
P1 = P2(1:L/2+1); 
P1(2:end-1) = 2*P1(2:end-1);
f = fs*(-L/2:L/2-1)/L; % per 1 Hz
figure;
stem(f,fftshift(P2)) % Shifts the zero to the center
title('Double-Sided Amplitude Spectrum of B0007')
xlabel('Frequency $(\frac{1}{167}$ Hz)', 'Interpreter', 'latex');
ylabel('|P(f)|')
%% Choice cut-off frequenices

scaling_number = 175;
scaling_factor = scaling_number/length(capacity_B0007);
LPF_Window = 22;
% Using Ideal LPF filter to filter to smooth high frequency componment
LPF_capacity_B0007 = fftshift(Y_fft);
LPF_capacity_B0007 =ifft(LPF_capacity_B0007(L/2-LPF_Window :L/2+LPF_Window),scaling_number);  % once choosing the cut_off frequency,using rectangular window to padding 0
%178 is the scalleing factor
figure;
Modified_LPF_capacity_B0007 = LPF_capacity_B0007 * scaling_factor;
plot(abs(Modified_LPF_capacity_B0007))
hold on;
plot(capacity_B0007)
legend('Capacity after using LPF with Padding','Raw Capacity')
title('Comparing of Filtering and raw data of B0007')
xlabel('Cycles');
ylabel("Capacity(Ah)")

%% plot the final filter output

startpoint = 6;
endpoint = length(capacity_B0007) + startpoint -1;

figure;
FinalModified_LPF_capacity_B0007 =Modified_LPF_capacity_B0007(startpoint:endpoint);
plot(abs(FinalModified_LPF_capacity_B0007),'blue')
hold on;
plot(capacity_B0007,'red')
legend('Final filtering Capacity','Raw Capacity')
title('Comparing of Final Filtering and raw data of B0007')
xlabel('Cycles');
ylabel("Capacity(Ah)")
rmse_B0007 = sqrt(sum(((capacity_B0007-abs(FinalModified_LPF_capacity_B0007)).^2)));
display(rmse_B0007)
%%  Do the same thing of B0018
fs = 1; %sampling  fs = 1 ,per cycle
L = length(capacity_B0018);  %length 167
Y_fft=fft(capacity_B0018);  % length 167
P2 = abs(Y_fft/L); 
P1 = P2(1:L/2+1); 
P1(2:end-1) = 2*P1(2:end-1);
f = fs*(-L/2:L/2-1)/L; % per 1 Hz
figure;
stem(f,fftshift(P2)) % Shifts the zero to the center
title('Double-Sided Amplitude Spectrum of B0018')
xlabel('Frequency $(\frac{1}{132}$ Hz)', 'Interpreter', 'latex');
ylabel('|P(f)|')

%% Choice cut-off frequenices

scaling_number = 140;
scaling_factor = scaling_number/length(capacity_B0018);
LPF_Window = 16;
% Using Ideal LPF filter to filter to smooth high frequency componment
LPF_capacity_B0018 = fftshift(Y_fft);
LPF_capacity_B0018 =ifft(LPF_capacity_B0018(L/2-LPF_Window :L/2+LPF_Window),scaling_number);  % once choosing the cut_off frequency,using rectangular window to padding 0
%178 is the scalleing factor
figure;
Modified_LPF_capacity_B0018 = LPF_capacity_B0018 * scaling_factor;
plot(abs(Modified_LPF_capacity_B0018))
hold on;
plot(capacity_B0018)
legend('Capacity after using LPF with Padding','Raw Capacity')
title('Comparing of Filtering and raw data of B0018')
xlabel('Cycles');
ylabel("Capacity(Ah)")

%% plot the final filter output

startpoint = 5;
endpoint = length(capacity_B0018) + startpoint -1;

figure;
FinalModified_LPF_capacity_B0018 =Modified_LPF_capacity_B0018(startpoint:endpoint);
plot(abs(FinalModified_LPF_capacity_B0018),'blue')
hold on;
plot(capacity_B0018,'red')
legend('Final filtering Capacity','Raw Capacity')
title('Comparing of Final Filtering and raw data of B0018')
xlabel('Cycles');
ylabel("Capacity(Ah)")
rmse_B0018 = sqrt(sum(((capacity_B0018-abs(FinalModified_LPF_capacity_B0018)).^2)));
display(rmse_B0018)
%%
rmse_LPF_B0005=rmse_B0005
rmse_LPF_B0006=rmse_B0006
rmse_LPF_B0007=rmse_B0007
rmse_LPF_B0018=rmse_B0018

%%
figure;

% B0005
subplot(2, 2, 1);
plot(abs(FinalModified_LPF_capacity_B0005), 'blue');
hold on;
plot(capacity_B0005, 'red');
legend('Final filtering Capacity', 'Raw Capacity');
title('B0005 Capacity');
xlabel('Cycles');
ylabel('Capacity (Ah)');

% B0006
subplot(2, 2, 2);
plot(abs(FinalModified_LPF_capacity_B0006), 'blue');
hold on;
plot(capacity_B0006, 'red');
legend('Final filtering Capacity', 'Raw Capacity');
title('B0006 Capacity');
xlabel('Cycles');
ylabel('Capacity (Ah)');

% B0007
subplot(2, 2, 3);
plot(abs(FinalModified_LPF_capacity_B0007), 'blue');
hold on;
plot(capacity_B0007, 'red');
legend('Final filtering Capacity', 'Raw Capacity');
title('B0007 Capacity');
xlabel('Cycles');
ylabel('Capacity (Ah)');

% B0018
subplot(2, 2, 4);
plot(abs(FinalModified_LPF_capacity_B0018), 'blue');
hold on;
plot(capacity_B0018, 'red');
legend('Final filtering Capacity', 'Raw Capacity');
title('B0018 Capacity');
xlabel('Cycles');
ylabel('Capacity (Ah)');

% Adjust the layout to prevent subplot titles and labels from overlapping
sgtitle('Comparison of Original vs. Low Pass Filter Smoothed Capacity for Batteries','FontSize', 12); % Super title for the entire figure
%% FFT about of y = -x + 1.85
% Define the sampling parameters
N = 167; % Number of samples
x = linspace(0, 1, N); % Sample points (from 0 to 1 for example)

% Define the function
y = -0.78*x + capacity_B0005(1);

% Compute the FFT
Y_fft = fft(y);

% Shift zero frequency component to the center of the array
Y_fft_shifted = fftshift(Y_fft);

% Frequency axis for double-sided spectrum
freq = (-N/2:N/2-1)*(1/N);

% Plot the double-sided spectrum
figure;
stem(freq, abs(Y_fft_shifted)/N); % Normalize the magnitude
title('Double-sided Amplitude Spectrum of y = -x + 1.85');
xlabel('Frequency $(\frac{1}{167}$ Hz)', 'Interpreter', 'latex');
ylabel('|Y(f)|');
