import pandapower as pp
import pandas as pd
import matplotlib.pyplot as plt
import pandapower.networks as nw
import seaborn as sns
import numpy as np
from numpy.random import choice
from numpy.random import normal
from pandapower.plotting.plotly import simple_plotly, pf_res_plotly
from pandapower.plotting.plotly.mapbox_plot import set_mapbox_token
from scipy.interpolate import make_interp_spline

set_mapbox_token('pk.eyJ1IjoidmljdG9ybXJmIiwiYSI6ImNsd2p3ZG92NTAwMjQycXFyNmRsYmFiOHYifQ.hXM5UlkNhQgzOz-cJyrvCw')

def load_network():
    return nw.mv_oberrhein("generation")

def violations(net):
    pp.runpp(net)
    if net.res_bus.vm_pu.max() > 1.05:
        return (True, "Limite de\nSobretensão")
    #if net.res_line.loading_percent.max() > 80:
    #    return (True, "Sobrecarregamento\nde linha")
    elif net.res_line.loading_percent.max() > 80:
        return (True, "Sobrecarregamento\nde linha")
    elif net.res_trafo.loading_percent.max() > 80:
        return (True, "Sobrecarregamento\nde transformador")
    else:
        return (False, None)
    
def chose_bus(net):
    return choice(net.load.bus.values)

def get_plant_size_mw():
    return normal(loc=0.5, scale=0.05)

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

def remover_indices(array, indices):
    for index in sorted(indices, reverse=True):
        del array[index]
    return array
    
def plot_line_chart(values):
    # Cria uma lista de índices para os pontos da linha
    #indices = list(range(len(values)))
    indices = np.arange(len(values))
    
    # Encontra os índices dos valores máximo e mínimo
    max_index = values.index(max(values))
    min_index = values.index(min(values))

    # Cria o gráfico de linha
    plt.plot(indices, values, color='blue') #marker='o')
    
    # Marca o valor máximo com um marcador especial (triângulo para cima)
    plt.plot(max_index, round(max(values), 3), 'g^', markersize=10, label=f'Valor máximo de tensão (pu): {round(max(values), 3)} (Barra {max_index})')
    
    # Marca o valor mínimo com um marcador especial (triângulo para baixo)
    plt.plot(min_index, round(min(values), 3), 'rv', markersize=10, label=f'Valor mínimo de tensão (pu): {round(min(values), 3)} (Barra {min_index})')

    # Adiciona título e rótulos
    plt.title('Tensão média por Barra', fontsize=20)
    plt.xlabel('Barras', fontsize=20)
    plt.ylabel('Tensão (pu)', fontsize=20)
    
    # Define os limites do eixo y
    plt.ylim(0.97, 1.05)
    plt.tick_params(axis='y', labelsize=18)
    plt.tick_params(axis='x', labelsize=18)

    # Adiciona rótulos aos eixos x e y
    #plt.xticks(indices, [f'{i+1}' for i in indices])

    # Adiciona a grade ao fundo do gráfico
    plt.grid(True)
    
    # Adiciona a legenda
    plt.legend(fontsize=18, loc="lower right")

    # Mostra o gráfico
    plt.show()
    
def create_boxplot(data):
    plt.figure(figsize=(8, 6))

    # Configurar o boxplot com tamanho reduzido
    sns.boxplot(data=data, width=0.25, boxprops=dict(alpha=0.7), flierprops=dict(markerfacecolor='r', markersize=5))

    # Adicionar linhas de grade
    plt.grid(color='gray', linestyle='--', linewidth=0.2, axis='y')
    
    # Calcular a mediana
    median = np.median(data)
    
    # Adicionar uma linha para a mediana
    #plt.axhline(y=median, color='blue', linestyle='--', linewidth=1.5, label=f'Mediana: {median:.2f}')
    plt.axhline(y=median, label=f'Mediana: {median:.2f}')

    # Título e rótulo
    #plt.title('Máxima Capacidade de Hospedagem', pad=20)
    plt.ylabel('Capacidade instalada [MW]', fontsize=16)

    # Adicionar legenda
    plt.legend(fontsize=16, loc="upper right")
    
    # Exibir o gráfico
    plt.show()


iterations = 10

results = pd.DataFrame(columns=["installed","violation"])
voltage_values = []

for i in range(iterations):
    net = load_network()
    svc_bus = chose_bus(net)
    # Alocação de SVC
    #pp.create_svc(net, chose_bus(net), x_l_ohm=1, x_cvar_ohm=-10, set_vm_pu=1., thyristor_firing_angle_degree=90, controllable=True)
    #pp.create_svc(net, bus=111, x_l_ohm=10, x_cvar_ohm=-10, set_vm_pu=1., thyristor_firing_angle_degree=90, controllable=True)
    #pp.create_svc(net, bus=84, x_l_ohm=10, x_cvar_ohm=-10, set_vm_pu=1., thyristor_firing_angle_degree=90, controllable=True)
    
    # Alocação de BESS
    #pp.create_storage(net, chose_bus(net), p_mw=2.5, max_e_mwh=5, soc_percent=40., q_mvar=0., min_e_mwh = 1, controllable=True)
    #pp.create_storage(net, chose_bus(net), p_mw=2.5, max_e_mwh=5, soc_percent=50., q_mvar=0., min_e_mwh = 1, controllable=True)
    #pp.create_storage(net, chose_bus(net), p_mw=2.5, max_e_mwh=5, soc_percent=70., q_mvar=0., min_e_mwh = 1, controllable=True)
    #pp.create_storage(net, chose_bus(net), p_mw=2.5, max_e_mwh=5, soc_percent=60., q_mvar=0., min_e_mwh = 1, controllable=True)
    installed_mw = 0
    while 1:
        violated, violation_type = violations(net)
        if violated:
            results.loc[i] = [installed_mw, violation_type]
            pp.runpp(net)
            vm_pu_values = net.res_bus['vm_pu'].tolist()
            voltage_values.append(vm_pu_values)
            break
        else:
            plant_size = get_plant_size_mw()
            pp.create_sgen(net, chose_bus(net), p_mw=plant_size, q_mvar=0)
            installed_mw += plant_size
            if installed_mw > 25:
                pp.runpp(net)
                vm_pu_values = net.res_bus['vm_pu'].tolist()
                voltage_values.append(vm_pu_values)
                #pf_res_plotly(net, on_map=True, projection='epsg:31467', map_style='dark')

media = calcular_media(voltage_values)
net.res_bus['vm_pu'] = media
pf_res_plotly(net, on_map=True, projection='epsg:31467', map_style='dark')
voltages = remover_indices(net.res_bus['vm_pu'].tolist(), [38, 176, 178])
plot_line_chart(voltages)
create_boxplot(results.installed)
print(svc_bus)
        