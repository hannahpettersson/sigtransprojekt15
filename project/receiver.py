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
    
    yr_filt = signal.lfilter(cb_d, ca_d, yr) #bandpass filter, vill bara släppa igenom våra wanted frequencies
    t_1 = np.arange(len(yr_filt)) /s_freq #tidsvektor, vi behöver rätt tidsindex

    # Calculate complex baseband signal
    ybi = 2 * yr_filt * np.cos(wc * t_1) # 2 för att vi tappar amplitud vid multiplication, in phase komponenten
    #
    ybi = signal.lfilter(b_lp_d, a_lp_d, ybi)
    ybq = 2 * yr_filt * np.sin(wc * t_1) # Lågpassfiltrerar och tar bort högfrekventa komponente, för att klara av fasförskjutningen, q komponenten
    ybq = signal.lfilter(b_lp_d, a_lp_d, ybq)

    yb = ybi + 1j*ybq
#below funkar för hello world men ej för längre meddelanden
    #gamma = 0.2 * np.max(np.abs(yb)) #skapa threshold baserad på max amplitud från signalen (strongest frequency)
    #start = np.argmax(np.abs(yb) > gamma) # Hittar första sampel där signalens magnitud överstiger threshold gamma

    #yb = yb[start:] # vi vill börha lyssna när signalen överstiger denna threshold -> blir av med allt brus innan start
    
    mag = np.abs(yb) # lite samma sak men här tar vi max apmlitud fron signalen
    active = mag > 0.2 * np.max(mag) # vi lyssnar aktivt när signalen är inom intervallet av 80%
# Find first and last active samples
    start = np.argmax(active) # börha lyssna
    end = len(active) - np.argmax(active[::-1]) 
    yb = yb[start:end]
    # Symbol decoding
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    br = wcs.decode_baseband_signal(yb, Tb, s_freq)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')


if __name__ == "__main__":    
    main()