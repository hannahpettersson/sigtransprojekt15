#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transmitter template for the wireless communication system project in Signals and
transforms

For plain text inputs, run:
$ python3 transmitter.py "Hello World!"

For binary inputs, run:
$ python3 transmitter.py -b 010010000110100100100001

2022-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd
import matplotlib.pyplot as plt
import wcslib as wcs

# TODO: Add relevant parameters to parameters.py
from parameters import dt,Tb,fs,Ac, wc

def main():
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
    sd.play(xt, 1/dt, blocking=True)
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10,15))
    
    #### TASK 4A ####
    plt.title("Task 4a")
    ax1.plot(t, xb, label="xb(t)")
    ax1.legend()
    ax1.set_xlabel("t (s)")
    ax1.set_ylabel("xb(t)")
    ax1.set_xlim(0, t1)
    ax1.grid()

    #### TASK 4B ####
    plt.title("Task 4b")
    ax2.plot(t, xm, label="xm(t)")
    ax2.legend()
    ax2.set_xlabel("t (s)")
    ax2.set_ylabel("xm(t)")
    ax2.set_xlim(0, 4*Tb)
    ax2.grid()
    
    #### TASK 4C ####
    plt.title("Task 4c")
    ax3.plot(t, yd, label="yd(t)")
    ax3.legend()
    ax3.set_xlabel("t (s)")
    ax3.set_ylabel("yd(t)")
    ax3.set_xlim(0, t1)
    ax3.grid()

    fig.savefig('lab1_task4.png')
    # plt.show()


if __name__ == "__main__":    
    main()
