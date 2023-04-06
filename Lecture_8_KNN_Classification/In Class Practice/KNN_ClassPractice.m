% Machine Learning.
% k-neareset neighbor classifier.
clc, clear; close all
% Load the training data and divide into the different classes
load  x0_new
load x1_new 
% plot the data
clf;
plot(x0(1,:), x0(2,:),'Bx');
hold on;
plot(x1(1,:), x1(2,:),'ro');
xlabel('x_0');
ylabel('x_1');
% --------------------------
figure; plot(x0(1,1:50), x0(2,1:50),'Bx');
hold on;
plot(x1(1,:), x1(2,:),'ro');
xlabel('x_0');
ylabel('x_1');
keyboard;
figure; plot(x0(1,1:50), x0(2,1:50),'Bx');
hold on;
plot(x1(1,:), x1(2,:),'ro');
xlabel('x_0');
ylabel('x_1');

load x0test_new
load x1test_new
plot(x0test(1,:), x0test(2,:),'kd');
plot(x1test(1,:), x1test(2,:),'kd');



