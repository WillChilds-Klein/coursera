function J = computeCost(X, y, theta)
%COMPUTECOST Compute cost for linear regression
%   J = COMPUTECOST(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta
%               You should set J to the cost.

square_sum = 0;
for i = 1:m;
    x_i = X(i,:);
    y_i = y(i);
    h_of_x = x_i * theta;
    square = (h_of_x - y_i)^2;
    square_sum += square;
end;

J = 1/(2*m) * square_sum;
% =========================================================================

end
