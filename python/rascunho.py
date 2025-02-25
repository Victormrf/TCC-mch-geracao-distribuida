import pandapower as pp
import pandas as pd
import matplotlib.pyplot as plt
import pandapower.networks as nw
import seaborn as sns
import pandapower.plotting.plotly as pplotly
from pandas import Series
from numpy.random import choice
from numpy.random import normal
from pandapower.plotting.plotly import pf_res_plotly
from pandapower.plotting.plotly import simple_plotly
from pandapower.plotting.plotly import vlevel_plotly
from pandapower.plotting.plotly.mapbox_plot import set_mapbox_token

def load_network():
    return nw.mv_oberrhein("generation")

net = load_network()
pf_res_plotly(net, on_map=True, map_style='dark')
set_mapbox_token('pk.eyJ1IjoidmljdG9ybXJmIiwiYSI6ImNsd2p3YTNhdTE0bDcybG13M2FwZzZreGgifQ.kzpTEncoRSEbyKLAD78k0w')
pplotly.geo_data_to_latlong(net, projection='epsg:31467') #transforming geodata to lat/long
#simple_plotly(net, on_map=True, projection='epsg:31467')
#simple_plotly(net)
#pf_res_plotly(net, on_map=True, map_style='dark')
#lc = pplotly.create_line_trace(net, net.line.index, color='purple')
#bc = pplotly.create_bus_trace(net, net.bus.index,size=10,color="orange",
#                              infofunc=Series(index=net.bus.index,
#                                              data=net.bus.name + '<br>' + net.bus.vn_kv.astype(str) + ' kV'))
#_ = pplotly.draw_traces(lc + bc, on_map=True, map_style='dark')

def calcular_media(arr):
    # Número de arrays dentro da lista
    num_arrays = len(arr)
    
    # Número de elementos em cada array (assumimos que todas as arrays têm o mesmo tamanho)
    num_elementos = len(arr[0])
    
    # Lista para armazenar as somas de cada índice
    somas = [0] * num_elementos
    
    # Itera sobre cada array
    for sub_array in arr:
        # Itera sobre cada elemento da array
        for i in range(num_elementos):
            somas[i] += sub_array[i]
    
    # Calcula a média dividindo cada soma pelo número de arrays
    medias = [soma / num_arrays for soma in somas]
    
    return medias

voltage_values = []

for i in range(3):  
    pp.runpp(net)
    vm_pu_values = net.res_bus['vm_pu'].tolist()
    voltage_values.append(vm_pu_values)

# Exemplo de uso
media = calcular_media(voltage_values)
media[0] = 0.66666
print(net.res_bus)
net.res_bus['vm_pu'] = media
print(net.res_bus)
#pf_res_plotly(net)


def plot_bar_chart(values):
    # Cria uma lista de índices para as barras
    indices = list(range(len(values)))

    # Cria o gráfico de barras
    plt.bar(indices, values, color='blue')

    # Adiciona título e rótulos
    plt.title('Valores de vm_pu')
    plt.xlabel('Índice')
    plt.ylabel('Valor de vm_pu')
    
    plt.ylim(0.90, 1.05)

    # Adiciona rótulos aos eixos x e y
    plt.xticks(indices, [f'{i+1}' for i in indices])

    # Mostra o gráfico
    plt.show()

# Chama a função para plotar o gráfico
#plot_bar_chart(vm_pu_values)

