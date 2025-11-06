% Median Filter 
% y = noisy signal

function med = median(y, k) 
    if nargin < 3 
        k = 15; 
    end 
    
    % return median filtered noisy signal
    med = movmedian(y, k); 

end