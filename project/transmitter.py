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
from scipy.signal import sosfreqz
import wcslib as wcs

# TODO: Add relevant parameters to parameters.py
from parameters import Tb, Ac, s_freq, Ts, wc, wp_dig, ws_dig, Ap, As, f_nyquist

#BP FILTER
Nc_d, w_c_d = signal.cheb2ord(wp_dig, ws_dig, Ap, As, analog=False)
Nc_d = int(np.ceil(Nc_d))
cb_d, ca_d = signal.iirdesign(wp=wp_dig, ws=ws_dig, gpass=Ap, gstop=As, ftype='cheby2', output='ba', analog=False)
wb_d, hc_d = signal.freqz(cb_d, ca_d)
f_bp_d = wb_d * f_nyquist / np.pi

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
    bs_tx = np.concatenate((bs, [1]))
    xb = wcs.encode_baseband_signal(bs_tx, Tb, s_freq)

    t = np.arange(0, xb.shape[0]) * Ts 
    xc = Ac * np.sin(wc * t)
    xm = xb * xc
    xt_filt = signal.lfilter(cb_d, ca_d, xm)
    # Ensure the signal is mono, then play through speakers
    xt_play = np.stack((xt_filt, np.zeros(xt_filt.shape)), axis=1)
    sd.play(xt_play, s_freq, blocking=True)

if __name__ == "__main__":    
    main()