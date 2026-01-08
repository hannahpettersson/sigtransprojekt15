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
from parameters import Tb, dt, alpha, wc, Ts, s_freq, Ac, data, wp_lp_norm_d, ws_lp_norm_d, Ap_lp, As_lp, f_nyquist, wp_dig, ws_dig, Ap, As

#BP FILTER
Nc_d, w_c_d = signal.cheb2ord(wp_dig, ws_dig, Ap, As, analog=False)
Nc_d = int(np.ceil(Nc_d))
cb_d, ca_d = signal.iirdesign(wp=wp_dig, ws=ws_dig, gpass=Ap, gstop=As, ftype='cheby2', output='ba', analog=False)
wb_d, hc_d = signal.freqz(cb_d, ca_d)
f_bp_d = wb_d * f_nyquist / np.pi

#LP FILTER
N_lp_d, Wn_lp_d = signal.buttord(wp_lp_norm_d, ws_lp_norm_d, Ap_lp, As_lp, analog=False)
N_lp_d = np.abs(np.ceil(N_lp_d))
b_lp_d, a_lp_d = signal.iirdesign(wp=wp_lp_norm_d, ws=ws_lp_norm_d, gpass=Ap_lp, gstop=As_lp, ftype='butter', output='ba', analog=False)
w_lp_d, h_lp_d = signal.freqz(b_lp_d, a_lp_d)
f_lp_d = w_lp_d * f_nyquist /np.pi  # convert from rad/s to Hz

# N_lp_d, Wn_lp_d = signal.cheb2ord(wp_lp_norm_d, ws_lp_norm_d, Ap, As, analog=False)
# N_lp_d = int(np.ceil(Nc_d))
# b_lp_d, a_lp_d = signal.iirdesign(wp=wp_lp_norm_d, ws=ws_lp_norm_d, gpass=Ap_lp, gstop=As_lp, ftype='cheby2', output='ba', analog=False)
# w_lp_d, h_lp_d = signal.freqz(cb_d, ca_d)
# f_lp_d = w_lp_d * f_nyquist /np.pi  # convert from rad/s to Hz

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
    
    yr_filt = signal.lfilter(cb_d, ca_d, yr) #bandpass filter
    t_1 = np.arange(len(yr_filt)) /s_freq

    # Calculate complex baseband signal
    ybi = yr_filt * 2 * np.cos(wc*t_1)
    ybi = signal.lfilter(b_lp_d, a_lp_d, ybi)
    ybq = yr_filt * (-2) * np.sin(wc*t_1)
    ybq = signal.lfilter(b_lp_d, a_lp_d, ybq)

    yb = ybi + 1j*ybq

    br = wcs.decode_baseband_signal(yb, Tb, s_freq)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')


if __name__ == "__main__":    
    main()