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

import wcslib as wcs

# TODO: Add relevant parameters to parameters.py
from parameters import Tb, dt, alpha, wc, Ts, s_freq, Ap_lp, As_lp, wp_lp_norm_d, ws_lp_norm_d, f_nyquist, Ac, data, bb, ab # ...

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
    yr = sd.rec(int(T/Ts), samplerate=s_freq, channels=1, blocking=True)
    yr = yr[:, 0]           # Remove second channel

    # TODO: Implement demodulation, etc. here
    # ...
    #bandpass filter
    # yr = signal.lfilter(bb, ab, yr)

    # cheby2 filter
    N_lp_d, Wn_lp_d = signal.buttord(wp_lp_norm_d, ws_lp_norm_d, Ap_lp, As_lp, analog=False)
    N_lp_d = np.abs(np.ceil(N_lp_d))
    b_lp_d, a_lp_d = signal.iirdesign(wp=wp_lp_norm_d, ws=ws_lp_norm_d, gpass=Ap_lp, gstop=As_lp, ftype='butter', output='ba', analog=False)

    # Lowpass filter coefficients: b_lp, a_lp
    w_lp_d, h_lp_d = signal.freqz(b_lp_d, a_lp_d)
    f_lp_d = w_lp_d * f_nyquist /np.pi  # convert from rad/s to Hz

    # Baseband signal
    t = np.arange(0, yr.shape[0]) * Ts  

    yd = yr * np.sin(wc * t)
    
    num = [alpha**2]
    den = [1, alpha, alpha**2]
    H = signal.TransferFunction(num, den)

    __, yb, __ = signal.lsim(H, yd, t)

    # Symbol decoding
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    br = wcs.decode_baseband_signal(yb, Tb, 1/Ts)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')


if __name__ == "__main__":    
    main()