#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：HPGCseismic 
@File    ：bandpass.py
@Author  ：weiyw
@Date    ：2022/11/18 21:21 
'''

import numpy as np
from scipy import signal


def bandpass(inarray=None, btype='bandpass', order=10, low=None, high=None, dt=0.001):
    '''
    A zero-phase filter
    :param inarray: 2D shot gather, [NT, NX]
    :param btype: {'lowpass', 'highpass', 'bandpass', 'bandstop'}
    :param order: default is 10
    :param low: lower band of filter
    :param high: high band of filter
    :param dt: unit is {s}
    :return: 2D shot gather after filtered

    Example:

    >> from HPGCseismic import waa
    >> readindata = np.load("sampleShotGather.npy")
    >> bandpassdata = waa.bandpass(inarray=readindata, btype='bandpass', order=5,  low=1, high=30, dt=0.001)

    '''

    NT, NX = inarray.shape
    fs = int(1 / dt)
    print(fs)
    t = np.linspace(0, NT * dt, NT, False)
    if btype == 'lowpass':
        sos = signal.butter(order, low, btype=btype, fs=fs, output='sos')
    elif btype == 'highpass':
        sos = signal.butter(order, high, btype=btype, fs=fs, output='sos')
    else:
        sos = signal.butter(order, [low, high], btype=btype, fs=fs, output='sos')

    ouarray = np.zeros_like(inarray)
    for ii in range(NX):
        sig = inarray[:, ii].copy()
        filtered = signal.sosfilt(sos, sig)
        ouarray[:, ii] = filtered

    return ouarray