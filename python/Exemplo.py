# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 20:04:33 2024

@author: Principal
"""

import pandapower as pp
import pandas as pd
#import matplotlib.pyplot as plt
#import pandapower.networks as nw
#from numpy.random import choice
#from numpy.random import normal

# Criando a rede
net = pp.create_empty_network()

# Criando as barras
b1 = pp.create_bus(net, vn_kv=20., name="Bus 1")
b2 = pp.create_bus(net, vn_kv=0.4, name="Bus 2")
b3 = pp.create_bus(net, vn_kv=0.4, name="Bus 3")
b4 = pp.create_bus(net, vn_kv=0.4, name="Bus 4")

# Criando os elementos associados as barras
pp.create_ext_grid(net, bus=b1, vn_pu=1.00, name = "Grid Connection")
pp.create_load(net, bus=b3, p_mw=0.01, q_mvar=0.005, name="Load")
pp.create_load(net, bus=b4, p_mw=0.01, q_mvar=0.005, name="Load2")

# Criando elementos de linha 
tid = pp.create_transformer(net, hv_bus=b1, lv_bus=b2, std_type="0.4 MVA 20/0.4 kV", name="Trafo")
pp.create_line(net, from_bus=b2, to_bus=b3, length_km=0.1, name="Line", std_type="NAYY 4x120 SE")
pp.create_line(net, from_bus=b1, to_bus=b4, length_km=0.1, name="Line2", std_type="NAYY 4x120 SE")

pp.runpp(net)
vm_pu_values = net.res_bus['vm_pu'].tolist()

array = [0, 1, 2, 3]
print(vm_pu_values)
#print(array)