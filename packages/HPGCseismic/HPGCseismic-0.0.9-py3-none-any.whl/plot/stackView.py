#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：HPGCseismic 
@File    ：stackView.py
@Author  ：weiyw
@Date    ：2022/11/18 21:29 
'''

# import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as pcl
# from matplotlib.font_manager import FontProperties

# SimHei = FontProperties(
#     fname='/home/wyw/anaconda3/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/SimHei.ttf')


def stackView(OUT=None, scale=0.1, title=None, ratio=16, nplot=None, namelist=None):
    sc1 = OUT.mean() - scale * OUT.std()
    sc2 = OUT.mean() + scale * OUT.std()
    cN = pcl.Normalize(vmin=sc1, vmax=sc2)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=120)
    # im = ax.imshow(OUT, aspect=16/400, cmap='seismic', norm=cN, interpolation='nearest')
    # im = ax.imshow(OUT, cmap='seismic', norm=cN, interpolation='bicubic', extent=[0,126,3,0])
    im = ax.imshow(OUT, cmap='seismic', norm=cN, interpolation='bicubic', extent=[0, 300, 80, 0])
    ax.set_aspect(ratio)  # 4
    #     ax.set_aspect(60) # 2
    #     plt.colorbar(im, shrink=0.3, orientation='horizontal')
    #     plt.axis('off')

    #     plt.ylabel(u'时间（秒）', fontsize=10, fontproperties=SimHei) # y轴标题
    #     plt.gca().invert_yaxis()
    #     plt.ylim([3, 0])

    nx = OUT.shape[1]
    #     print(nx)

    #     for i in range(1, nplot):
    #         plt.axvline( int((i)*nx/nplot), color='black') #, linewidth=2 )
    plt.title(namelist)
    return ax
