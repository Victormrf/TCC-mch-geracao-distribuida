import pandapower as pp
from pandapower.networks import mv_oberrhein
import pandas as pd
import numba
import matplotlib.pyplot as plt
import pandapower.networks as nw
import seaborn as sns
from numpy.random import choice
from numpy.random import normal
from pandapower.plotting.plotly import pf_res_plotly

def load_network():
    return nw.mv_oberrhein("generation")
    #return nw.create_cigre_network_lv()


def violations(net):
    pp.runpp(net)
    if net.res_line.loading_percent.max() > 100:
        return (True, "Sobrecarregamento\nde linha")
    elif net.res_trafo.loading_percent.max() > 100:
        return (True, "Sobrecarga\nde transformador")
    elif net.res_bus.vm_pu.max() > 1.05:
        return (True, "Limite de\nSobretensão")
    #if net.res_bus.vm_pu.max() > 1.05:
    #    return (True, "Limite de\nSobretensão")
    #if net.res_trafo.loading_percent.max() > 100:
    #    return (True, "Sobrecarga\nde transformador")
    #if net.res_line.loading_percent.max() > 100:
    #    return (True, "Sobrecarregamento\nde linha")
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

def plot_bar_chart(values):
    # Cria uma lista de índices para as barras
    indices = list(range(len(values)))

    # Cria o gráfico de barras
    plt.bar(indices, values, color='blue')

    # Adiciona título e rótulos
    plt.title('Valores de vm_pu')
    plt.xlabel('Índice')
    plt.ylabel('Valor de vm_pu')
    
    plt.ylim(0.90, 1.10)

    # Adiciona rótulos aos eixos x e y
    plt.xticks(indices, [f'{i+1}' for i in indices])

    # Mostra o gráfico
    plt.show()

iterations = 100


results = pd.DataFrame(columns=["installed","violation"])
voltage_values = []

for i in range(iterations):
    net = load_network()
    installed_mw = 0
    while 1:
        violated, violation_type = violations(net)
        if violated:
            #results.loc[i] = [installed_mw, violation_type, voltage_values]
            results.loc[i] = [installed_mw, violation_type]
            
            break
        else:
            plant_size = get_plant_size_mw()
            pp.create_sgen(net, chose_bus(net), p_mw=plant_size, q_mvar=0)
            installed_mw += plant_size
            pp.runpp(net)
            vm_pu_values = net.res_bus['vm_pu'].tolist()
            voltage_values.append(vm_pu_values)
 
#print(voltage_values)
media = calcular_media(voltage_values)
net.res_bus['vm_pu'] = media
pf_res_plotly(net)
plot_bar_chart(media)
print(media)

plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.rc('legend', fontsize=18)
plt.rc('axes', labelsize=20)
plt.rcParams['font.size'] = 20

sns.set_style("whitegrid", {'axes.grid': False})
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
ax = axes[0]
sns.boxplot(results.installed, width=.1, ax=ax, orient="v")
ax.set_xticklabels([""])
ax.set_ylabel("Capacidade instalada [MW]")

ax = axes[1]
ax.axis("equal")
results.violation.value_counts().plot(kind="pie", ax=ax, autopct=lambda x:"%.0f %%"%x)
ax.set_ylabel("")
ax.set_xlabel("")
fig.suptitle("CIGRE - Baixa tensão sem GD prévia", fontsize=16)
sns.despine()
plt.tight_layout()            