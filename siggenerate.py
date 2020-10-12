import numpy as np
import matplotlib.pyplot as plt  # library for plotting
from scipy.fftpack import fft, fftshift
import random
import math, cmath


# Convert single precision IEEE 754 float to hex
def floatToHex(a):
    afx = float.hex(a)
    # print(afx)
    afxstr = str(afx)
    afxstrlen = len(afxstr)
    # print(afxstr)
    if (afxstr[0] == '-'):
        signbit = 1
    else:
        signbit = 0
    # print(signbit)

    i = afxstr.index('p')
    # print(i)
    p = int(afxstr[i + 2:len(afxstr)])
    if (afxstr[i + 1] == "+"):
        psign = 1
    else:
        psign = -1
    # print(p)
    # print(psign)
    plen = len(str(p))

    if (a == 0):
        pbias = 0
    else:
        pbias = p * psign + 127
    # print(pbias)

    pt = afxstr.index('.')
    # print(pt)
    # print(len(afxstr))
    mantissa = afxstr[pt + 1:afxstrlen - plen - 2]
    # print(mantissa)
    mantissa = int(mantissa, 16) >> 29
    # print(hex(mantissa))

    hexfloat = str(hex(mantissa | (pbias << 23) | (signbit << 31)))

    return hexfloat


# Convert 32-bit hex to single precision IEEE 754 float
def hexToFloat(a):
    SIGNMASK = 1 << 31
    EXPMASK = 0xFF << 23
    FRACTION = 0x7FFFFF
    LEADINGBIT = 1 << 23
    aint = int(a, 16)
    # print(aint)
    astr = str(aint)
    # print(astr)
    if (((aint & SIGNMASK) >> 31) == 1):
        signbit = -1
    else:
        signbit = 1
    exponent = ((aint & EXPMASK) >> 23) - 127;
    fraction = (aint & FRACTION) | LEADINGBIT;
    result = float(fraction) / float(2 ** (23 - exponent))
    result = result * signbit;
    # print(result)

    return result;


def sine_wave_gen(f, fs, phase, nsamples):
    """
    Generate sine wave signal with the following parameters
    Parameters:
        f : frequency of sine wave in Hertz
        overSampRate : oversampling rate (integer)
        phase : desired phase shift in radians
        nCyl : number of cycles of sine wave to generate
    Returns:
        (t,g) : time base (t) and the signal g(t) as tuple
    Example:
        f=10; overSampRate=30;
        phase = 1/3*np.pi;nCyl = 5;
        (t,g) = sine_wave(f,overSampRate,phase,nCyl)
    """
    ts = 1 / fs

    t = np.arange(0, nsamples * ts, ts)  # time base
    g = np.sin(2 * np.pi * f * t + phase)  # replace with cos if a cosine wave is desired
    return (t, g)  # return time base and signal g(t) as tuple


N = 128  # 128-point
fs = 100  # sampling frequency in Hz
nsamples = N

# signal 1
f1 = 10  # frequency = 10 Hz
phase1 = 0  # 1/3*np.pi #phase shift in radians
# desired number of cycles of the sine wave
(t1, x1) = sine_wave_gen(f1, fs, phase1, nsamples)  # function call

# signal 2
f2 = 30  # frequency = 10 Hz
phase2 = 0  # 1/3*np.pi #phase shift in radians
(t2, x2) = sine_wave_gen(f2, fs, phase2, nsamples)  # function call

# signal 3
f3 = 20  # frequency = 10 Hz
phase3 = 0  # 1/3*np.pi #phase shift in radians
(t3, x3) = sine_wave_gen(f3, fs, phase3, nsamples)  # function call

# AWGN
noise = np.zeros(nsamples)
magnitude = 2.0
for i in range(0, nsamples):
    noise[i] = magnitude * (random.random() - 0.5)

x = x1 + x2 + x3 + noise

# write time domain test file

writefile = open('signalfile.txt', 'w')
for i in range(0, len(x)):
    writefile.write(floatToHex(x[i]))
    writefile.write('\n')

writefile.close()

# plt.plot(t,x) # plot using pyplot library from matplotlib package
# plt.title('Sine wave f='+str(f)+' Hz') # plot title
# plt.xlabel('Time (s)') # x-axis label
# plt.ylabel('Amplitude') # y-axis label
# plt.show() # display the figure

# read time domain test file
readfile = open('signalfile.txt', 'r')

fpstr = readfile.readline()
i = 0
while (fpstr != ""):
    x[i] = hexToFloat(fpstr)
    i = i + 1
    fpstr = readfile.readline()

readfile.close()

# compute FFT
NFFT = N
xfft = fft(x, NFFT)
# X=fftshift(xfft) #uncomment if generating shifted fft results from signalfile

# write real and imaginary scalars into respective text files in hex format
writefile = open('realfile.txt', 'w')
for i in range(0, len(xfft)):
    writefile.write(floatToHex(xfft[i].real))
    writefile.write('\n')

writefile.close()

writefile = open('imagfile.txt', 'w')
for i in range(0, len(xfft)):
    writefile.write(floatToHex(xfft[i].imag))
    writefile.write('\n')

writefile.close()

# read real fft results
readfile = open('realfile.txt', 'r')

fpstr = readfile.readline()
i = 0
while (fpstr != ""):
    xfft[i] = hexToFloat(fpstr)
    i = i + 1
    fpstr = readfile.readline()

readfile.close()

# read imag fft results
readfile = open('imagfile.txt', 'r')

fpstr = readfile.readline()
i = 0
while (fpstr != ""):
    xfft[i] = xfft[i] + hexToFloat(fpstr) * 1j
    i = i + 1
    fpstr = readfile.readline()

readfile.close()

X = fftshift(xfft)

# plot N-pt shifted fft result (magnitude only) in frequency domain

fVals = np.arange(start=-NFFT / 2, stop=NFFT / 2) * fs / NFFT
plt.plot(fVals, np.abs(X), 'b')
plt.title(str(NFFT) + '-point FFT - with FFTShift')
plt.xlabel('Frequency (Hz)')
plt.ylabel('|DFT Values|')
plt.xlim(-fs / 2, fs / 2)
plt.xticks(np.arange(-fs / 2, fs / 2 + 1, fs / 5))
plt.show()

