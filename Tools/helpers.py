import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

from pyprodrisk import ProdriskSession


def run_session(plant_name, method, inflow_model,cvar=[0,0],summag=False,tempdata=False,spillPenalty=0):
    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)

    local_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter",plant_name, plant_name + " data")

    name = f"{method}_{plant_name}_{inflow_model}"

    prodrisk.load_model_yaml(file_path=local_dir,file_name=plant_name + ".yaml")
    prodrisk.load_data_h5(file_path=local_dir,file_name=plant_name + ".h5")

    prodrisk.temp_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\tempdata",name)
    prodrisk.log_file_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Logfiles"
    prodrisk.mpi_path = r"C:\Program Files\Microsoft MPI\bin"            # absolute path to mpi executables
    prodrisk.prodrisk_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268777wpdm_prodrisk_cvar_win\prodrisk_cvar_win"     # absolute path to Prodrisk executables
    prodrisk.keep_working_directory = tempdata                              # remove temporary files after the simulation
    prodrisk.write_penalty_logfiles = 1

    if inflow_model == "lg":
        prodrisk.inflow_model = "lognormal"
    if inflow_model == "pca":
        prodrisk.inflow_model = "principal"
    if inflow_model == "res":
        prodrisk.inflow_model = "residual"

    if cvar != [0,0]:

        prodrisk.cvar = cvar[0]
        prodrisk.cvar_weight = cvar[1]
    
    if spillPenalty != 0:
        prodrisk.overflow_cost = spillPenalty

    status = prodrisk.run()

    run_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Finished Runs")


    prodrisk.dump_model_yaml(file_path=run_folder,file_name=name,direction="both")
    prodrisk.dump_data_h5(file_path=run_folder,file_name=name,direction="both")

    return


def load_session(plant_name, method, inflow_model):

    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)
    
    folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Finished Runs")

    file = method + "_" + plant_name + "_" + inflow_model

    prodrisk.load_model_yaml(file_path=folder,file_name=file)
    prodrisk.load_data_h5(file_path=folder,file_name=file)

    return prodrisk

def plot_reservoir_volumes(plant_name, method, inflow_model):

    prodrisk = load_session(plant_name,method,inflow_model)

    if plant_name == "Fjone":
        nape_mod = prodrisk.model.module["nape"]
        rolle_mod = prodrisk.model.module["rolleivstadvatn"]
        sand_mod = prodrisk.model.module["sandvatn"]

        nape_vol = nape_mod.reservoirVolume.get()
        rolle_vol = rolle_mod.reservoirVolume.get()
        sand_vol = sand_mod.reservoirVolume.get()

        index = nape_vol.index

        total_vol = nape_vol.values + rolle_vol.values + sand_vol.values

        percs = [0,25,50,75,100]


        plot_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results\Volume"

        # ----- Total Volume fig ----- 
        total_perc = np.percentile(total_vol,percs,axis=1)
        fig_total, ax_total = plt.subplots(figsize=(10,10),sharey=True)

        for p, vals in zip(percs,total_perc):
            ax_total.plot(index, vals, label=f"{p}th percentile")
        ax_total.plot(index,np.mean(total_vol,axis=1),label="Mean")
        ax_total.set(title=method + ", " + inflow_model + " total volume",ylabel=r"Volume [Mm$^3$]",xlabel="Time")
        ax_total.grid()
        ax_total.legend()


        path_total = os.path.join(plot_folder, method + "_" + inflow_model + "Fjone_total_volume.png")
        fig_total.savefig(path_total, dpi=300, bbox_inches='tight')


        # ----- Nape Volume fig -----
        nape_perc = np.percentile(nape_vol.values,percs,axis=1)
        fig_nape, ax_nape = plt.subplots(figsize=(10,10),sharey=True)
        for p, vals in zip(percs,nape_perc):
            ax_nape.plot(index, vals, label=f"{p}th percentile")
        ax_nape.plot(index,np.mean(nape_vol.values,axis=1),label="Mean")
        ax_nape.set(title=method + ", " + inflow_model ,ylabel=r"Volume [Mm$^3$]",xlabel="Time")
        ax_nape.grid()
        ax_nape.legend()

        path_nape = os.path.join(plot_folder, method + "_" + inflow_model + "Fjone_nape_volume.png")
        fig_nape.savefig(path_nape, dpi=300, bbox_inches='tight')




    return 



def topology(plant_name):

    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)
    

    data_path = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, plant_name + " data")

    prodrisk.load_model_yaml(file_path=data_path,file_name=plant_name)
    prodrisk.load_data_h5(file_path=data_path,file_name=plant_name)

    path = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Results",plant_name + "_topology.png")

    prodrisk.plot_topology(path)

    # print(prodrisk.model.area.get_object_names())

    return 


def plot_overflow(plant_name, method, inflow_model):

    prodrisk = load_session(plant_name,method,inflow_model)

    magazines = prodrisk.model.module.get_object_names()

    fig, axes = plt.subplots(1, len(magazines),figsize=(20,10),sharey=True)

    for i in range(len(magazines)):
        mod = prodrisk.model.module[magazines[i]]
        overflow = mod.overflow.get()
        axes[i].fill_between(overflow.index, np.percentile(overflow.values[:,:],0,axis=1),np.percentile(overflow.values[:,:],100,axis=1),alpha=0.2)
        axes[i].plot(overflow.mean(axis=1))
        axes[i].set(title=magazines[i],xlabel="Time",ylabel="Overflow")
        axes[i].grid()
    fig.suptitle(f"Overflow with {method} and {inflow_model}")

    plot_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results\Overflow"
    path = os.path.join(plot_folder, method + "_" + inflow_model + "Fjone_overflow.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')

    return

def plot_total_overflow(plant_name, method, inflow_model):

    prodrisk = load_session(plant_name,method,inflow_model)

    fig,ax = plt.subplots(figsize=(20,10))

    area = prodrisk.model.area["my_area"]
    tot_overflow = area.total_reservoir_overflow.get()

    # ax.fill_between(tot_overflow.index, np.percentile(tot_overflow.values[:,:],0,axis=1),np.percentile(tot_overflow.values[:,:],100,axis=1),alpha=0.2)
    ax.plot(tot_overflow.mean(axis=1))
    ax.set(title="Total reservoir overflow",xlabel="Time",ylabel="Overflow",ylim=(0,0.07))
    ax.grid()

    plot_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results\Overflow"
    path = os.path.join(plot_folder, method + "_" + inflow_model + "Fjone_total_overflow.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')



def plot_inflow(plant_name, method, inflow_model):

    prodrisk = load_session(plant_name,method,inflow_model)

    magazines = prodrisk.model.module.get_object_names()

    fig, axes = plt.subplots(1, len(magazines),figsize=(20,10),sharey=True)

    for i in range(len(magazines)):
        mod = prodrisk.model.module[magazines[i]]
        inflow = mod.localInflow.get()
        axes[i].fill_between(inflow.index, np.percentile(inflow.values[:,:],0,axis=1),np.percentile(inflow.values[:,:],100,axis=1),alpha=0.2)
        axes[i].plot(inflow.mean(axis=1))
        axes[i].set(title=magazines[i],xlabel="Time",ylabel="Inflow")
        axes[i].grid()
    fig.suptitle(f"Inflow with {method} and {inflow_model}")
    
    plot_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results\Inflow"
    path = os.path.join(plot_folder, method + "_" + inflow_model + "Fjone_inflow.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')

    return

def plot_discharge(plant_name, method, inflow_model):
    prodrisk = load_session(plant_name,method,inflow_model)

    magazines = prodrisk.model.module.get_object_names()

    fig, axes = plt.subplots(1, len(magazines),figsize=(20,10),sharey=True)

    for i in range(len(magazines)):
        mod = prodrisk.model.module[magazines[i]]
        discharge = mod.discharge.get()
        axes[i].fill_between(discharge.index, np.percentile(discharge.values[:,:],0,axis=1),np.percentile(discharge.values[:,:],100,axis=1),alpha=0.2)
        axes[i].plot(discharge.mean(axis=1))
        axes[i].set(title=magazines[i],xlabel="Time",ylabel="Discharge")
        axes[i].grid()
    fig.suptitle(f"Discharge with {method} and {inflow_model}")
    
    plot_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results\Discharge"
    path = os.path.join(plot_folder, method + "_" + inflow_model + "Fjone_discharge.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')

    return

def plot_production(plant_name, method, inflow_model):
    prodrisk = load_session(plant_name,method,inflow_model)

    magazines = prodrisk.model.module.get_object_names()

    fig, axes = plt.subplots(1, len(magazines),figsize=(20,10),sharey=True)

    for i in range(len(magazines)):
        mod = prodrisk.model.module[magazines[i]]
        production = mod.production.get()
        axes[i].fill_between(production.index, np.percentile(production.values[:,:],0,axis=1),np.percentile(production.values[:,:],100,axis=1),alpha=0.2)
        axes[i].plot(production.mean(axis=1))
        axes[i].set(title=magazines[i],xlabel="Time",ylabel="Production")
        axes[i].grid()
    fig.suptitle(f"Production with {method} and {inflow_model}")
    
    plot_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results\Production"
    path = os.path.join(plot_folder, method + "_" + inflow_model + "Fjone_production.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')

    return

def plot_bypass(plant_name, method, inflow_model):
    prodrisk = load_session(plant_name,method,inflow_model)

    magazines = prodrisk.model.module.get_object_names()

    fig, axes = plt.subplots(1, len(magazines),figsize=(20,10),sharey=True)

    for i in range(len(magazines)):
        mod = prodrisk.model.module[magazines[i]]
        bypass = mod.bypass.get()
        # axes[i].fill_between(bypass.index, np.percentile(bypass.values[:,:],0,axis=1),np.percentile(bypass.values[:,:],100,axis=1),alpha=0.2)
        axes[i].plot(bypass.mean(axis=1))
        axes[i].set(title=magazines[i],xlabel="Time",ylabel="Bypass")
        axes[i].grid()
    fig.suptitle(f"Bypass with {method} and {inflow_model}")
    
    plot_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results\Bypass"
    path = os.path.join(plot_folder, method + "_" + inflow_model + "Fjone_bypass.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')

    return


def tail_metrics(values, alpha):
    n = len(values)
    k = int(np.ceil(alpha * n))
    sorted_vals = np.sort(values)
    worst = sorted_vals[:k]

    var = sorted_vals[k - 1]
    cvar = np.mean(worst)

    return var, cvar



def income(plant_name, method, inflow_model):

    prodrisk = load_session(plant_name, method, inflow_model)

    nscenarios = prodrisk.n_scenarios
    area = prodrisk.model.area["my_area"]

    volume = area.total_reservoir_volume.get().to_numpy()
    production = area.total_production.get().to_numpy()
    price = area.output_price.get().to_numpy()

    mean_price = np.mean(price, axis=0)

    # Scenario-wise calculations
    scenario_income = np.sum(production * price, axis=0)


    endValue = volume[-1, :] * mean_price
    startValue = volume[0, :] * mean_price

    scenario_adjusted = scenario_income + endValue - startValue

    # Average results
    avg_income = np.mean(scenario_income)
    avg_adjusted = np.mean(scenario_adjusted)

    var10, cvar10 = tail_metrics(scenario_adjusted, 0.10)
    var20, cvar20 = tail_metrics(scenario_adjusted, 0.20)

    # print(f"Average income: {avg_income:.2f}")
    # print(f"Adjusted income: {avg_adjusted:.2f}")
    # print(f"Worst 10% VaR: {var10:.2f}, CVaR: {cvar10:.2f}")
    # print(f"Worst 20% VaR: {var20:.2f}, CVaR: {cvar20:.2f}")

    return [avg_adjusted, cvar10]






def water_value(plant_name,method,inflow_model):


    prodrisk = load_session(plant_name, method, inflow_model)

    area = prodrisk.model.area["my_area"]

    water_vals = area.water_value_result.get()

    min_water_val = water_vals.values[0].min()
    max_water_val = water_vals.values[0].max()
    mean_water_val = water_vals.values[0].mean()
    std_water_val = water_vals.values[0].std()

    summary_df = pd.DataFrame({
        "Min": [min_water_val],
        "Max": [max_water_val],
        "Mean": [mean_water_val],
        "STD" : [std_water_val]

    }, index=[method + " " + inflow_model])

    return summary_df

    
    


def neg_inflow(plant_name, method, inflow_model):

    prodrisk = load_session(plant_name, method, inflow_model)

    magazines = prodrisk.model.module.get_object_names()

    
    data = {}

    for mag in magazines:
        mod = prodrisk.model.module[mag]
        neg_inflow = mod.average_neg_inflow_back.get()
        data[mag] = neg_inflow.mean()   

    df = pd.DataFrame(data, index=[method + " " + inflow_model])

    return df


def inflow_weight(plant_name, method, inflow_model):

    prodrisk = load_session(plant_name, method, inflow_model)

    magazines = prodrisk.model.inflowSeries.get_object_names()

    for mag in magazines:
        inflow = prodrisk.model.inflowSeries[mag]
        weight = inflow.outcomeProbability.get()
        print(weight)




