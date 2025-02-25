import pandapower as pp
import pandas as pd
import matplotlib.pyplot as plt
import pandapower.networks as nw
import seaborn as sns
from numpy.random import choice
from numpy.random import normal

def load_network():
    return nw.create_cigre_network_mv(with_der=False)

def violations(net):
    pp.runpp(net)
    if net.res_bus.vm_pu.max() > 1.05:
        return (True, "Limite de\nSobretensão")
    elif net.res_line.loading_percent.max() > 100:
        return (True, "Sobrecarregamento\nde linha")
    elif net.res_trafo.loading_percent.max() > 100:
        return (True, "Sobrecarga\nde transformador")
    else:
        return (False, None)
    
def chose_bus(net):
    return choice(net.load.bus.values)

def get_plant_size_mw():
    return normal(loc=0.5, scale=0.05)

iterations = 100
results = pd.DataFrame(columns=["installed","violation"])

for i in range(iterations):
    net = load_network()
    installed_mw = 0
    while 1:
        violated, violation_type = violations(net)
        if violated:
            results.loc[i] = [installed_mw, violation_type]
            break
        else:
            plant_size = get_plant_size_mw()
            pp.create_sgen(net, chose_bus(net), p_mw=plant_size, q_mvar=0)
            installed_mw += plant_size
            
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
sns.despine()
plt.tight_layout()