import numpy as np
import wcslib as wcs

# TODO: Add your parameters here. You might need to add other parameters as well.
channel_id = 17
Tb = 0.02
fs = 4400 # används ej i lab 2
dt = 1/22050 # Används ej i lab 2
Ac = 1
fc = 4400
bs = 1 / Tb
wc = 2 * np.pi * fc    # rad/s
alpha = 2 * np.pi * 200
# Ar = |H(w)| * Ac
tr = 1
phi = -wc*tr

# Lab 2
K = 5
s_freq = fc * K
Ts = 1 / s_freq 
f_nyquist = s_freq/2 #22000 Hz

Ap = 2
As = 40

Ap_lp = 0.8 #passband ripple in db
As_lp = 40 #stopband attenuation in db
Wp_lp = 600 #HZ passband edge
Ws_lp = 1100 #Hz stopband edge
wp_arr = [4300, 4500]
ws_arr = [4250, 4550]

# Analog filter parameters (BP, LP)

wp = 2*np.pi * np.array([4300, 4500])
ws = 2*np.pi * np.array([4250, 4550])

wp_lp_norm = Wp_lp*(2*np.pi)
ws_lp_norm = Ws_lp*(2*np.pi)

# Digital filter parameters (BP, LP)

wp_dig = np.array(wp_arr) / f_nyquist
ws_dig = np.array(ws_arr) / f_nyquist

wp_lp_norm_d = Wp_lp/f_nyquist
ws_lp_norm_d = Ws_lp/f_nyquist


# Message to be transmitted
data = "Hello World!"