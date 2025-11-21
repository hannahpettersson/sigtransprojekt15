#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receiver template for the wireless communication system project in Signals and
transforms

2022-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd
import matplotlib.pyplot as plt
import wcslib as wcs

# TODO: Add relevant parameters to parameters.py 
from parameters import dt,Tb,fs,Ac,wc,alpha,bs

### FROM transmitter.py ###
parser = argparse.ArgumentParser(
    prog='transmitter',
    description='Acoustic wireless communication system -- transmitter.'
)
parser.add_argument(
    '-b',
    '--binary',
    help='message is a binary sequence',
    action='store_true'
)
parser.add_argument('message', help='message to transmit', nargs='?')
args = parser.parse_args()

if args.message is None:
    args.message = 'Hello World!'

# Set parameters
data = args.message

# Convert string to bit sequence or string bit sequence to numeric bit
# sequence
if args.binary:
    bs = np.array([bit for bit in map(int, data)])
else:
    bs = wcs.encode_string(data)

# Transmit signal
print(f'Sending: {data} (no of bits: {len(bs)}; message duration: {np.round(len(bs)*Tb, 1)} s).')

# Encode baseband signal
# TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
xb = wcs.encode_baseband_signal(bs, Tb, 1/dt)       # Task 4a)

# TODO: Implement transmitter code here
t = np.arange(0, xb.shape[0]) * dt  
t1 = 10*Tb
# plot = int(np.ceil(t1/dt))

# Ensure the signal is mono, then play through speakers
xc = Ac * np.sin(wc * t)                            # Task 4b
xm = xb * xc
xt = xm
yd = xm * np.sin(wc * t)

xt = np.stack((xt, np.zeros(xt.shape)), axis=1)
### END transmitter.py ###

def main():
    parser = argparse.ArgumentParser(
        prog='receiver',
        description='Acoustic wireless communication system -- receiver.'
    )
    parser.add_argument(
        '-d',
        '--duration',
        help='receiver recording duration',
        type=float,
        default=10
    )
    args = parser.parse_args()

    # Set parameters
    T = args.duration

    # Receive signal
    print(f'Receiving for {T} s.')
    yr = sd.rec(int(T/dt), samplerate=1/dt, channels=1, blocking=True)
    yr = yr[:, 0]           # Remove second channel

    # TODO: Implement demodulation, etc. here
    # ...
    num = [alpha**2]
    den = [1, alpha, alpha**2]
    H = signal.TransferFunction(num, den)
    
    w, mag, phase = H.bode()
    # mag_log = 20*np.log10(mag) # dB
    phase_rad = (phase * np.pi) / 180

    #### Task 4d) ####
    fig, ax4 = plt.subplots(2, 1)
    ax4[0].semilogx(w, mag)
    # ax4[0].semilogx(w, mag_log)
    ax4[0].set_ylabel("Magnitude (dB)")
    ax4[0].grid()

    ax4[1].semilogx(w, phase_rad)
    ax4[1].set_ylabel("Phase (rad)")
    ax4[1].set_xlabel("Frequency (rad/s)")
    ax4[1].grid()
    fig.savefig('lab1_task4d.png')
    # plt.show()

     #### Task 4e ####
    __, yb, __ = signal.lsim(H, yd, t)
    
    fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,10))
    plt.title("Task 4e")
    ax1.plot(t, xb, label="xb(t)")
    ax1.legend()
    ax1.set_xlabel("t (s)")
    ax1.set_ylabel("xb(t)")
    ax1.set_xlim(0, t1)
    ax1.grid()

    ax2.plot(t, yb, label="yb(t)")
    ax2.legend()
    ax2.set_xlabel("t (s)")
    ax2.set_ylabel("yb(t)")
    ax2.set_xlim(0, t1)
    ax2.grid()

    fig2.savefig("lab1_task4e")

    # # Baseband signal
    # ybi = 
    # ybq = 
    # yb = ybi + 1j*ybq 

    # Symbol decoding
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    br = wcs.decode_baseband_signal(yb, Tb, 1/dt)
    # data_rx = wcs.decode_string(br)
    print(f'Received: {br} (no of bits: {len(br)}).')


if __name__ == "__main__":    
    main()
