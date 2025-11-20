import numpy as np
import wcslib as wcs

# TODO: Add your parameters here. You might need to add other parameters as well.
channel_id = 17
Tb = 0.01
fs = 4400
dt = 1/22050
Ac = 1
fc = 4400
bs = 1 / Tb
wc = 27646    # rad/s
alpha = 2*np.pi*200


# Message to be transmitted
data = "Hello World!"