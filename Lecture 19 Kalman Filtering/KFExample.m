clc, clear; close all;

% Define the system:
N = 1000; % number of time steps
dt = 0.001; % sampling time (sec)
t = dt*(1:N); % time vector
A = [ 1 dt; 0 1]; % state matrix
B = [ -1/2*dt^2; -dt]; % input matrix
C = [ 1 0]; % observation matrix
I  = eye(2) 
Q = I; % state noise covariance
u = 9.8;

% Define the initial position and velocity (the states)
y0 = 100;% m
v0 = 0; % m/s

% Initialize the true state vector
xt = zeros(2,N); % true state vector
xt(:,1) = [y0; v0];

for k = 2:N
    xt(:,k) = A*xt(:,k-1)+B*u;
end

% ------------------
R = 4;
v = 0+sqrt(R)*randn(1,N);
y = C*xt+v;


% ---------------------------
% Implementation of Kalman Filter
x = zeros(2,N);
% Guess
x(:,1)= [ 105;0]; % Initial Guess

% Initialize the covariance matrix
P = [ 10 0; 0 0.1];

for k = 2:N
    % Predict the state vector
    x(:,k) = A*x(:,k-1)+B*u;
    % Predict the covariance matrix
    P = A*P*A'+Q;
    % predict Kalman Gain
    K  =P*C'*pinv(C*P*C'+R);

    % update the state vector
    x(:,k) = x(:,k)+K*(y(k)-C*x(:,k));
    % Update the covariance matrix
    P = (I-K*C)*P;
end


figure;  plot(t,x(1,:)); hold on; plot(t,xt(1,:)); legend('Estimsted','True')







%-------------------------







