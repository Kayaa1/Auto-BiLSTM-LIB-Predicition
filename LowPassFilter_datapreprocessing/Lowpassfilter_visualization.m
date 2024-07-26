% Parameters for the ideal low-pass filter
Omega_c = pi / 4;  % Normalized cutoff frequency
N = 100;            % Number of points for impulse response - centered at zero

% Define the normalized frequency range
Omega = linspace(-pi, pi, 1000);  % Use more points for a smoother plot

% Create the frequency response H(Omega)
H_Omega = double(abs(Omega) <= Omega_c);

% Define the time vector for the impulse response (using samples)
n = -(N-1)/2:(N-1)/2; % Ensure n includes the range from -8 to 8


% Plot the frequency response
figure;
plot(Omega, H_Omega);
title('Frequency Response H(\Omega) of Ideal Low-Pass Filter');
xlabel('\Omega (normalized frequency)');
ylabel('Magnitude');
xlim([-pi pi])
xticks(-pi:pi/2:pi)
xticklabels({'-\pi','\pi/2','0','\pi/2','\pi'})
axis tight;  % Fit the plot to the data
grid on;

% Define the range and constants
n = -16:1:16;
Omega_c = pi/4;
syms y(x)
y(x) = piecewise(x==0,(Omega_c /pi),x~=0,(Omega_c /pi).*(sin(x.*Omega_c)./(x.*Omega_c)));
h_n = double(subs(y(x),x,n)); % Symbolic substitution

% Plot h_n
figure;
stem(n, h_n, 'filled');
xlim([-16 16])
title('Impulse Response h(n) of Ideal Low-Pass Filter');
xlabel('n (samples)');
ylabel('Amplitude');
grid on;
