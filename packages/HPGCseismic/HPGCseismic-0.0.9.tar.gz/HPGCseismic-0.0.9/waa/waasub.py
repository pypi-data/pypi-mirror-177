#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：HPGCseismic 
@File    ：waasub.py
@Author  ：weiyw
@Date    ：2022/11/18 21:09 
'''

import numpy as np

def waa_moving_average(array1d=None, winb=None):
    atmp = np.ones( (len(array1d)) )
    kernel = np.ones( (winb) )
    mask = np.convolve(atmp, kernel, mode='same')
    avArray = np.convolve(array1d, kernel, mode='same')
    return avArray / mask


def waa_median_average(array2d=None, nMedian=3):
    '''
    array2d:
        1st axis: time
        2nd axis: space
    '''
    NT, NX = array2d.shape
    assert NX >= 3
    maArray = np.zeros((NT))

    for ii in range(NT):
        tmpA = array2d[ii, :].copy()
        # calculate median average
        tmpMed = np.zeros((nMedian))
        for jj in range(nMedian):
            tmpMed[jj] = np.median(tmpA)
            tmpA[tmpA == tmpMed[jj]] = tmpA.min()
        maArray[ii] = tmpMed.mean()
    return maArray


def calculate_coef(wma1d=None, array2d=None, scale=1, atten=10):
    NT, NX = array2d.shape
    Mask = np.zeros((NT, NX))
    # calculate std of seismic data
    wmstd = np.std(array2d, axis=1)

    for ii in range(NT):
        thres = wma1d[ii] + scale * wmstd[ii]
        thres_low = wma1d[ii] - scale * wmstd[ii]
        tmpA = array2d[ii, :].copy()
        for jj in range(NX):
            if tmpA[jj] > thres:
                Mask[ii, jj] = np.exp(-atten * (tmpA[jj] - thres))
            elif tmpA[jj] < thres_low:
                Mask[ii, jj] = np.exp(-atten * (thres_low - tmpA[jj]))
            else:
                Mask[ii, jj] = 1
    return Mask
