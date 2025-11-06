% y = noisy signal
% n = column vector of noise profile
% nfft = length of FFT
% hopSize = hop length
% xhat = denoised signal

function [xhat] = wienerFilter(y, n, nfft, noverlap, fs)
    
    %create hann window
    window = hann(nfft, "periodic");

    % pwelch = power spectral density estimate using hann window, input sample
    % rate fs and "two sided" estimate
    Syy = pwelch(y, window, noverlap, nfft, fs, 'twosided'); % power spectral density of noisy signal
    Snn = pwelch(n, window, noverlap, nfft, fs, 'twosided'); % power spectral density of noise profile 
    
    % compute transfer function H(w)
    H = 1 - abs(Snn./Syy);

    % make sure values are positive
    H = max(0, H);
    %H(H<0) = 0; %other option

    % convert to time domain
    h = ifft(H);
    
    % FIR filtering
    % xhat = fftfilt(h, y, nfft); %should do the same thing as next two lines
    xhat = fftfilt(h, y);
    xhat = xhat(1:length(y));

end