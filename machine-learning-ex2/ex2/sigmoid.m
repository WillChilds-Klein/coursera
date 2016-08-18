function g = sigmoid(z)
%SIGMOID Compute sigmoid functoon
%   J = SIGMOID(z) computes the sigmoid of z.

% You need to return the following variables correctly 
g = zeros(size(z));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the sigmoid of each value of z (z can be a matrix,
%               vector or scalar).
if (isvector(z) || ismatrix(z))
    for i = 1:rows(z)
        for j = 1:columns(z)
            g(i,j) = single_sigmoid(z(i,j));
        end
    end
elseif (isscalar(z))
    g = single_sigmoid(z);
end
% =============================================================

end

function g = single_sigmoid(z)
    g = 1 / (1 + e^(-1*z));
end
