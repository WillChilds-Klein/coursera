function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Note: grad should have the same dimensions as theta
%

% === Calculate J === %
outer_sum = 0;
for i = 1:m
    x_i = X(i,:)';                          % transpose to make col vector
    y_i = y(i);
    h_of_x = sigmoid(theta' * x_i);
    left_term = (-1*y_i) * log(h_of_x);
    right_term = (1 - y_i) * log(1 - h_of_x);
    outer_sum += left_term - right_term;
end
J = (1/m) * outer_sum;
% =================== %

% === Calculate grad === %
for j = 1:length(grad)
    grad_sum = 0;
    for i = 1:m
        x_i = X(i,:)';
        y_i = y(i);
        h_of_x = sigmoid(theta' * x_i);
        grad_sum += (h_of_x - y_i) * x_i(j);
    end
    grad(j) = (1/m) * grad_sum;
end
% ====================== %

% =============================================================

end
