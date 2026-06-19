import tracker
import numpy as np

def rtn_frame(line1, line2):

    e, r, v = tracker.propagate_satellite(line1, line2)

    r = np.array(r)
    v = np.array(v)

    R_hat = r/np.linalg.norm(r)

    h = np.cross(r,v)

    N_hat = h/np.linalg.norm(h)

    T_hat = np.cross(N_hat, R_hat)

    return R_hat, T_hat, N_hat