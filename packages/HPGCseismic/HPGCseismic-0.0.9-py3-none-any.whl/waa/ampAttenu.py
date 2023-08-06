#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：HPGCseismic 
@File    ：waa.py
@Author  ：weiyw
@Date    ：2022/11/18 21:07 
'''

# external
import numpy as np

# internal
from .waasub import waa_moving_average, waa_median_average, calculate_coef

# workflow
# class ampAttenu():
def ampAttenu(oridata=None):
    '''

    :param oridata: a 2D shot gather, [NT, NX].
    :return: attenuated shot gatehr, [NT, NX].

    Example:

    >> from HPGCseismic import waa
    >> readindata = np.load("sampleShotGather.npy")
    >> denoisedata = waa.ampAttenu(readindata)
s
    '''


    NT, NX = oridata.shape
    # prepare for denosing
    readin = oridata.copy()
    #     print(f"debug: {readin}")
    # get all absolute data
    readin[readin < 0] *= -1
    #     print(f"debug: {readin}")

    # smooth time axis
    Asmooth = np.zeros_like(readin)
    for ii in range(NX):
        Asmooth[:, ii] = waa_moving_average(array1d=readin[:, ii], winb=3)
    # get median average of space axis
    Bmeave = waa_median_average(array2d=readin, nMedian=3)  # 1D vector: length is NT

    # calculate mask
    Cmask = calculate_coef(wma1d=Bmeave, array2d=readin, scale=2, atten=1e2)

    # denosing
    Outdata = Cmask * oridata
    return Outdata