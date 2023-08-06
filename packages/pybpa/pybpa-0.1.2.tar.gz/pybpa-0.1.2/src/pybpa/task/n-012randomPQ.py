# -*- coding:utf-8 -*-
"""
# Name:         dlgxa: n_sample-012randomPQ
# Author:       MilkyDesk
# Date:         2022/3/10 16:28
# Description:
#   生成N-0/1/2不同拓扑下的随机出力
1. 超参数配置方法
2. for 拓扑:
       for 出力: 生成新的dat并保存到指定文件夹
"""

# ------------------------- params --------------------------

# ------------------------- params --------------------------
from ..utils.utils import GenLoadGenerator, LHSGenerator, topo_generator, LSDWriter
import numpy as np
from ..dat.bpa_dat import DAT
import networkx as nx
import os

pqpqvt = np.zeros([6, 39], dtype=np.bool_)
pqpqvt[2, 30:38] = True
dat_path = r'E:\Data\transient_stability\39\bpa\dlgxa版本/N-012/0_100_0.dat'
lsd_path = r'E:\Data\transient_stability\39\bpa\dlgxa版本/N-012/0.lsd'
dat = DAT.build_from(dat_path)
# generator = LHSGenerator(dat, pqpqvt, 0.4, truncate=0.9973)  # 3sigma
generator = LHSGenerator(dat, pqpqvt, 0.01, truncate=1)
lsd_writer = LSDWriter(lsd_path)
topo_generator(0, 3, dat, r'E:\Data\transient_stability\39\bpa\dlgxa版本/N-3/', 1, generator, make0=False,
               lsd_writer=lsd_writer)
# topo_generator(2, -1, dat, r'E:\Data\transient_stability\39\bpa/12_u40_sample20/', 20, generator, prefix=['1', '26'])
# todo 要生成单个拓扑下的很多很多个样本，至少1000.

