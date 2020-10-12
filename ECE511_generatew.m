N = 256;
% used dftmtx instead after research
% imaginary_vals = zeros(N,N);
% real_vals = zeros(N,N);
% count = 1;
% for row = 1:N
%     for col = 1:N
%         value = 2*pi*(row-1)*(col-1)/N;
%         eulers = exp(-1j*value);
%         imaginary_vals(row,col) = round(imag(eulers),10);
%         real_vals(row,col) = round(real(eulers),10);
%         count = count + 1;
%     end
% end

imaginary_vals = num2hex(single(imag(dftmtx(N))));
real_vals = num2hex(single(real(dftmtx(N))));
imag_name = sprintf('%d_bit_imag.txt', N);
real_name = sprintf('%d_bit_real.txt', N);
writematrix(imaginary_vals, imag_name, 'delimiter', ',');
writematrix(real_vals, real_name, 'delimiter', ',');

% 
% file_ID = fopen(file_name, 'w');
% fprintf(file_ID, 'imag: .word ');
% for row = 1:N
%         fprintf(file_ID, '\t %s\n', imaginary_vals(128-row*8:128-row*8+8));
% end
% fclose(file_ID);
