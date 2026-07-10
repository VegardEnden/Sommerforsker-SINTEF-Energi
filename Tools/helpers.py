import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

from pyprodrisk import ProdriskSession


plt.rcParams["axes.labelsize"] = 15
plt.rcParams["axes.titlesize"] = 18


def run_session(plant_name, method, inflow_model,cvar=[0,0],summag=[0,0,0],week=[],min=[],max=[],tempdata=True,
                spillPenalty=0,bypassPenalty=0, magPenalty = "", series=0,nprinc= 0, princDisc= [], saveInflow=False,loadInflow=False):
    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)

    local_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter",plant_name, plant_name + " data")

    name = f"{method}_{plant_name}_{inflow_model}"

    prodrisk.load_model_yaml(file_path=local_dir,file_name=plant_name + ".yaml")
    prodrisk.load_data_h5(file_path=local_dir,file_name=plant_name + ".h5")

    temp_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\tempdata", name)
    prodrisk.temp_dir = temp_dir
    prodrisk.log_file_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Logfiles"
    prodrisk.mpi_path = r"C:\Program Files\Microsoft MPI\bin"            # absolute path to mpi executables
    prodrisk.prodrisk_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\cvar-stefan\cvar-prototype"     # absolute path to Prodrisk executables
    prodrisk.keep_working_directory = tempdata                             
    prodrisk.write_penalty_logfiles = 1
    prodrisk.n_processes = 8
    prodrisk.prodrisk_variant = "prodrisk_cplex_ms_mpi.exe"

    if inflow_model == "lg":
        prodrisk.inflow_model = "lognormal"
    elif inflow_model == "pca":
        prodrisk.inflow_model = "principal"
        prodrisk.n_principal_comp.set(nprinc)
        prodrisk.n_principal_comp_discrete_values.set(princDisc)

    elif inflow_model == "res":
        prodrisk.inflow_model = "residual"

    if cvar != [0,0]:
        prodrisk.cvar = cvar[0]
        prodrisk.cvar_weight = cvar[1]
    
    if spillPenalty != 0:
        if magPenalty != "":
            mod = prodrisk.model.module[magPenalty]
            mod.ForwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
            mod.BackwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
        else:
            magazines = prodrisk.model.module.get_object_names()
            for mag in magazines:
                mod = prodrisk.model.module[mag]
                mod.ForwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[spillPenalty]*prodrisk.n_weeks))
                mod.BackwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
    if bypassPenalty != 0:

        if magPenalty != "":
            mod = prodrisk.model.module[magPenalty]
            mod.ForwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[bypassPenalty]*prodrisk.n_weeks))
            mod.BackwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[bypassPenalty]*prodrisk.n_weeks))
        else:
            magazines = prodrisk.model.module.get_object_names()
            for mag in magazines:
                mod = prodrisk.model.module[mag]
                mod.ForwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[bypassPenalty]*prodrisk.n_weeks))
                mod.BackwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[bypassPenalty]*prodrisk.n_weeks))

    if series == 1:
        prodrisk.is_series_simulation = series

    if loadInflow:
        area = prodrisk.model.area["my_area"]
        prob = pd.read_parquet(os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow", plant_name + "_probabilities.parquet"))
        area.lognormal_probabilities.set(prob)
        for ser in prodrisk.model.inflowSeries.get_object_names():
            centers = pd.read_parquet(os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow", f"{plant_name}_{ser}_centers.parquet"))
            prodrisk.model.inflowSeries[ser].lognormal_centers.set(centers)
        prodrisk.read_lognormal_model.set(1)


    run_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Finished Runs")

    if summag != [0,0,0]:
        prodrisk.summag_min_penalty = summag[0]
        prodrisk.summag_max_penalty = summag[1]
        prodrisk.summag_forward = summag[2]

        area = prodrisk.model.area["my_area"]
        area.summag_min.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in week], data=min))
        area.summag_max.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in week], data=max))

        prodrisk._pb_api.GenerateProdriskFiles()

        input()

        status = prodrisk._pb_api.RunProdrisk()

        return     


    #prodrisk._pb_api

    status = prodrisk.run()


    prodrisk.dump_model_yaml(file_path=run_folder,file_name=name,direction="both")
    prodrisk.dump_data_h5(file_path=run_folder,file_name=name,direction="both")

    if saveInflow:
        inflow_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow")
        prob_path = os.path.join(inflow_folder, plant_name + "_probabilities.parquet")
        area = prodrisk.model.area["my_area"]
        area.lognormal_probabilities.get().to_parquet(prob_path)
        for ser in prodrisk.model.inflowSeries.get_object_names():
            centers = prodrisk.model.inflowSeries[ser].lognormal_centers.get()
            centers.to_parquet(os.path.join(inflow_folder, f"{plant_name}_{ser}_centers.parquet"))



    return

def run_session_old(plant_name, method, inflow_model,cvar=[0,0],summag=[0,0,0],week=[],min=[],max=[],tempdata=True,
                spillPenalty=0,bypassPenalty=0, magPenalty = "", series=0,nprinc= 0, princDisc= [], saveInflow=False,loadInflow=False):
    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)

    local_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter",plant_name, plant_name + " data")

    name = f"{method}_{plant_name}_{inflow_model}"

    prodrisk.load_model_yaml(file_path=local_dir,file_name=plant_name + ".yaml")
    prodrisk.load_data_h5(file_path=local_dir,file_name=plant_name + ".h5")

    temp_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\tempdata", name)
    prodrisk.temp_dir = temp_dir
    prodrisk.log_file_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Logfiles"
    prodrisk.mpi_path = r"C:\Program Files\Microsoft MPI\bin"            # absolute path to mpi executables
    prodrisk.prodrisk_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268777wpdm_prodrisk_cvar_win\prodrisk_cvar_win"    # absolute path to Prodrisk executables
    prodrisk.keep_working_directory = tempdata                             
    prodrisk.write_penalty_logfiles = 1
    prodrisk.n_processes = 8
    prodrisk.prodrisk_variant = "prodrisk_cplex_ms_mpi.exe"

    if inflow_model == "lg":
        prodrisk.inflow_model = "lognormal"
    elif inflow_model == "pca":
        prodrisk.inflow_model = "principal"
        prodrisk.n_principal_comp.set(nprinc)
        prodrisk.n_principal_comp_discrete_values.set(princDisc)

    elif inflow_model == "res":
        prodrisk.inflow_model = "residual"

    if cvar != [0,0]:
        prodrisk.cvar = cvar[0]
        prodrisk.cvar_weight = cvar[1]
    
    if spillPenalty != 0:
        if magPenalty != "":
            mod = prodrisk.model.module[magPenalty]
            mod.ForwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
            mod.BackwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
        else:
            magazines = prodrisk.model.module.get_object_names()
            for mag in magazines:
                mod = prodrisk.model.module[mag]
                mod.ForwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[spillPenalty]*prodrisk.n_weeks))
                mod.BackwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
    if bypassPenalty != 0:

        if magPenalty != "":
            mod = prodrisk.model.module[magPenalty]
            mod.ForwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[bypassPenalty]*prodrisk.n_weeks))
            mod.BackwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[bypassPenalty]*prodrisk.n_weeks))
        else:
            magazines = prodrisk.model.module.get_object_names()
            for mag in magazines:
                mod = prodrisk.model.module[mag]
                mod.ForwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[bypassPenalty]*prodrisk.n_weeks))
                mod.BackwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[bypassPenalty]*prodrisk.n_weeks))

    if series == 1:
        prodrisk.is_series_simulation = series

    if loadInflow:
        area = prodrisk.model.area["my_area"]
        prob = pd.read_parquet(os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow", plant_name + "_probabilities.parquet"))
        area.lognormal_probabilities.set(prob)
        for ser in prodrisk.model.inflowSeries.get_object_names():
            centers = pd.read_parquet(os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow", f"{plant_name}_{ser}_centers.parquet"))
            prodrisk.model.inflowSeries[ser].lognormal_centers.set(centers)
        prodrisk.read_lognormal_model.set(1)


    run_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Finished Runs")

    status = prodrisk.run()


    prodrisk.dump_model_yaml(file_path=run_folder,file_name=name,direction="both")
    prodrisk.dump_data_h5(file_path=run_folder,file_name=name,direction="both")

    if saveInflow:
        inflow_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow")
        prob_path = os.path.join(inflow_folder, plant_name + "_probabilities.parquet")
        area = prodrisk.model.area["my_area"]
        area.lognormal_probabilities.get().to_parquet(prob_path)
        for ser in prodrisk.model.inflowSeries.get_object_names():
            centers = prodrisk.model.inflowSeries[ser].lognormal_centers.get()
            centers.to_parquet(os.path.join(inflow_folder, f"{plant_name}_{ser}_centers.parquet"))



    return


def run_timedependent_session(plant_name, inflow_model, tempdata=True, spillPenalty=0,bypassPenalty=0, magPenalty = "", loadInflow=False, saveInflow=False):
    
    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)

    local_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter",plant_name, plant_name + " data")

    name = f"Time-dependent_{plant_name}_{inflow_model}"

    prodrisk.load_model_yaml(file_path=local_dir,file_name=plant_name + ".yaml")
    prodrisk.load_data_h5(file_path=local_dir,file_name=plant_name + ".h5")

    temp_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\tempdata", name)
    prodrisk.temp_dir = temp_dir
    prodrisk.log_file_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Logfiles"
    prodrisk.mpi_path = r"C:\Program Files\Microsoft MPI\bin"            # absolute path to mpi executables
    prodrisk.prodrisk_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\cvar-timedependent"    # absolute path to Prodrisk executables
    prodrisk.keep_working_directory = tempdata                             
    prodrisk.write_penalty_logfiles = 1
    prodrisk.n_processes = 8
    prodrisk.prodrisk_variant = "prodrisk_cplex_ms_mpi.exe"
    
    if spillPenalty != 0:
        if magPenalty != "":
            mod = prodrisk.model.module[magPenalty]
            mod.ForwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
            mod.BackwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
        else:
            magazines = prodrisk.model.module.get_object_names()
            for mag in magazines:
                mod = prodrisk.model.module[mag]
                mod.ForwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[spillPenalty]*prodrisk.n_weeks))
                mod.BackwardSpillingCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[spillPenalty]*prodrisk.n_weeks))
    if bypassPenalty != 0:

        if magPenalty != "":
            mod = prodrisk.model.module[magPenalty]
            mod.ForwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[bypassPenalty]*prodrisk.n_weeks))
            mod.BackwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                        data=[bypassPenalty]*prodrisk.n_weeks))
        else:
            magazines = prodrisk.model.module.get_object_names()
            for mag in magazines:
                mod = prodrisk.model.module[mag]
                mod.ForwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[bypassPenalty]*prodrisk.n_weeks))
                mod.BackwardBypassCostEnergy.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in range(prodrisk.n_weeks)],
                                                            data=[bypassPenalty]*prodrisk.n_weeks))
    if loadInflow:
        area = prodrisk.model.area["my_area"]
        prob = pd.read_parquet(os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow", plant_name + "_probabilities.parquet"))
        area.lognormal_probabilities.set(prob)
        for ser in prodrisk.model.inflowSeries.get_object_names():
            centers = pd.read_parquet(os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow", f"{plant_name}_{ser}_centers.parquet"))
            prodrisk.model.inflowSeries[ser].lognormal_centers.set(centers)
        prodrisk.read_lognormal_model.set(1)
    
    prodrisk._pb_api.GenerateProdriskFiles()

    input("Add riskparam.dat")

    status = prodrisk._pb_api.RunProdrisk()

    run_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Finished Runs")

    prodrisk.dump_model_yaml(file_path=run_folder,file_name=name,direction="both")
    prodrisk.dump_data_h5(file_path=run_folder,file_name=name,direction="both")

    if saveInflow:
        inflow_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow")
        prob_path = os.path.join(inflow_folder, plant_name + "_probabilities.parquet")
        area = prodrisk.model.area["my_area"]
        area.lognormal_probabilities.get().to_parquet(prob_path)
        for ser in prodrisk.model.inflowSeries.get_object_names():
            centers = prodrisk.model.inflowSeries[ser].lognormal_centers.get()
            centers.to_parquet(os.path.join(inflow_folder, f"{plant_name}_{ser}_centers.parquet"))

    
    return


def run_session_summag(plant_name,inflow_model,tempdata=True,loadInflow=False,saveInflow=False,
                       nprinc=0,princDisc=[],summag=[0,0,0],week=[],min=[],max=[]):

    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\prapi\dist\release64\6.0.1_2026-07-10_36225e8f5\Prodrisk_API_6.0.1_2026-07-10_36225e8f5\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)

    local_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter",plant_name, plant_name + " data")

    name = f"Summag_{plant_name}_{inflow_model}"

    prodrisk.load_model_yaml(file_path=local_dir,file_name=plant_name + ".yaml")
    prodrisk.load_data_h5(file_path=local_dir,file_name=plant_name + ".h5")

    temp_dir = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\tempdata", name)
    prodrisk.temp_dir = temp_dir
    prodrisk.log_file_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Logfiles"
    prodrisk.mpi_path = r"C:\Program Files\Microsoft MPI\bin"            # absolute path to mpi executables
    prodrisk.prodrisk_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\ltm_core\dist\x64\windows\release\package\prodrisk_core"   # absolute path to Prodrisk executables
    prodrisk.keep_working_directory = tempdata                             
    prodrisk.write_penalty_logfiles = 1
    prodrisk.n_processes = 8
    prodrisk.prodrisk_variant = "prodrisk_cplex_ms_mpi.exe"

    if inflow_model == "lg":
        prodrisk.inflow_model = "lognormal"
    elif inflow_model == "pca":
        prodrisk.inflow_model = "principal"
        prodrisk.n_principal_comp.set(nprinc)
        prodrisk.n_principal_comp_discrete_values.set(princDisc)

    elif inflow_model == "res":
        prodrisk.inflow_model = "residual"

    if loadInflow:
        area = prodrisk.model.area["my_area"]
        prob = pd.read_parquet(os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow", plant_name + "_probabilities.parquet"))
        area.lognormal_probabilities.set(prob)
        for ser in prodrisk.model.inflowSeries.get_object_names():
            centers = pd.read_parquet(os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow", f"{plant_name}_{ser}_centers.parquet"))
            prodrisk.model.inflowSeries[ser].lognormal_centers.set(centers)
        prodrisk.read_lognormal_model.set(1)

    if summag != [0,0,0]:
        prodrisk.summag_min_penalty = summag[0]
        prodrisk.summag_max_penalty = summag[1]
        prodrisk.summag_forward = summag[2]

        area = prodrisk.model.area["my_area"]
        area.summag_min.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in week], data=min))
        area.summag_max.set(pd.Series(index=[prodrisk.start_time + pd.Timedelta(weeks=w) for w in week], data=max))


    run_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Finished Runs")

    status = prodrisk.run()


    prodrisk.dump_model_yaml(file_path=run_folder,file_name=name,direction="both")
    prodrisk.dump_data_h5(file_path=run_folder,file_name=name,direction="both")

    if saveInflow:
        inflow_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Inflow")
        prob_path = os.path.join(inflow_folder, plant_name + "_probabilities.parquet")
        area = prodrisk.model.area["my_area"]
        area.lognormal_probabilities.get().to_parquet(prob_path)
        for ser in prodrisk.model.inflowSeries.get_object_names():
            centers = prodrisk.model.inflowSeries[ser].lognormal_centers.get()
            centers.to_parquet(os.path.join(inflow_folder, f"{plant_name}_{ser}_centers.parquet"))



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

def plot_reservoir_volumes(plant_name, method, inflow_model,lim,week_marker=[]):

    prodrisk = load_session(plant_name,method,inflow_model)

    magazines = prodrisk.model.module.get_object_names()
    
    biggest = ""
    max_vol = 0
    total_vol = np.zeros_like(prodrisk.model.module[magazines[0]].reservoirVolume.get().values)

    for mag in magazines:
        max_volume = prodrisk.model.module[mag].rsvMax.get()
        if max_volume > max_vol:
            max_vol = max_volume
            biggest = mag
        total_vol += prodrisk.model.module[mag].reservoirVolume.get().values

    individ_vol = prodrisk.model.module[biggest].reservoirVolume.get()
    index = individ_vol.index

    percs = [0,25,50,75,100]


    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Volume")

    # ----- Total Volume fig ----- 
    total_perc = np.percentile(total_vol,percs,axis=1)
    fig_total, ax_total = plt.subplots(figsize=(10,10),sharey=True)

    for p, vals in zip(percs,total_perc):
        ax_total.plot(index, vals, label=f"{p}th percentile")
    ax_total.plot(index,np.mean(total_vol,axis=1),label="Mean",lw=3,color="black")

    for marker in week_marker:
        if isinstance(marker, (int, np.integer)):
            target_time = index[0] + pd.Timedelta(weeks=marker)
            if isinstance(index, pd.DatetimeIndex):
                pos = np.argmin(np.abs(index - target_time))
                ax_total.axvline(index[pos], linestyle="--", color="gray", alpha=0.7)
        elif marker in index:
            ax_total.axvline(marker, linestyle="--", color="gray", alpha=0.7)

    ax_total.set(title=method + ", " + inflow_model + " total volume",ylabel=r"Volume [Mm$^3$]",xlabel="Time",ylim=lim)
    ax_total.grid()
    ax_total.legend()


    path_total = os.path.join(plot_folder, method + "_" + inflow_model + plant_name + "_total_volume.png")
    fig_total.savefig(path_total, dpi=300, bbox_inches='tight')

    if len(magazines) != 1:
        # ----- Largest magazine Volume fig -----
        individ_perc = np.percentile(individ_vol.values,percs,axis=1)
        fig_individ, ax_individ = plt.subplots(figsize=(10,10),sharey=True)
        for p, vals in zip(percs,individ_perc):
            ax_individ.plot(index, vals, label=f"{p}th percentile")
        ax_individ.plot(index,np.mean(individ_vol.values,axis=1),label="Mean",lw=3,color="black")

        for marker in week_marker:
            if isinstance(marker, (int, np.integer)):
                target_time = index[0] + pd.Timedelta(weeks=marker)
                if isinstance(index, pd.DatetimeIndex):
                    pos = np.argmin(np.abs(index - target_time))
                    ax_individ.axvline(index[pos], linestyle="--", color="gray", alpha=0.7)
            elif marker in index:
                ax_individ.axvline(marker, linestyle="--", color="gray", alpha=0.7)


        ax_individ.set(title=method + ", " + inflow_model + "_" + biggest ,ylabel=r"Volume [Mm$^3$]",xlabel="Time",ylim=(0,1.2*max_vol))
        ax_individ.grid()
        ax_individ.legend()

        path_individ = os.path.join(plot_folder, method + "_" + inflow_model + plant_name + "_"+ biggest + "_volume.png")
        fig_individ.savefig(path_individ, dpi=300, bbox_inches='tight')


    return 

def plot_reservoir_volumes_series(plant_name, method, inflow_model,lim):

    prodrisk = load_session(plant_name,method,inflow_model)

    magazines = prodrisk.model.module.get_object_names()
    
    biggest = ""
    max_vol = 0
    total_vol = np.zeros_like(prodrisk.model.module[magazines[0]].reservoirVolume.get().values)

    for mag in magazines:
        max_volume = prodrisk.model.module[mag].rsvMax.get()
        if max_volume > max_vol:
            max_vol = max_volume
            biggest = mag
        total_vol += prodrisk.model.module[mag].reservoirVolume.get().values

    individ_vol = prodrisk.model.module[biggest].reservoirVolume.get()
    index = individ_vol.index

    n = 35

    arr = np.round(np.linspace(0, n-1, 5)).astype(int)
    

    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Volume")

    # ----- Total Volume fig ----- 
    fig_total, ax_total = plt.subplots(figsize=(10,10),sharey=True)

    for i in arr:
        ax_total.plot(index, total_vol[:, i], label=f"Scenario{i+1}")
    ax_total.plot(index,np.mean(total_vol,axis=1),label="Mean",lw=3,color="black")
    ax_total.set(title=method + ", " + inflow_model + " total volume",ylabel=r"Volume [Mm$^3$]",xlabel="Time",ylim=lim)
    ax_total.grid()
    ax_total.legend()


    path_total = os.path.join(plot_folder, method + "_" + inflow_model + plant_name + "_total_volume.png")
    fig_total.savefig(path_total, dpi=300, bbox_inches='tight')

    if len(magazines) != 1:
        # ----- Largest magazine Volume fig -----
        fig_individ, ax_individ = plt.subplots(figsize=(10,10),sharey=True)
        for i in arr:
            ax_individ.plot(index, individ_vol.values[:, i], label=f"Scenario{i+1}")
        ax_individ.plot(index,np.mean(individ_vol.values,axis=1),label="Mean",lw=3,color="black")
        ax_individ.set(title=method + ", " + inflow_model ,ylabel=r"Volume [Mm$^3$]",xlabel="Time",ylim=(0,1.2*max_vol))
        ax_individ.grid()
        ax_individ.legend()

        path_individ = os.path.join(plot_folder, method + "_" + inflow_model + plant_name + "_"+ biggest + "_volume.png")
        fig_individ.savefig(path_individ, dpi=300, bbox_inches='tight')


def compare_volumes(plant_name, method1, method2, inflow_model1, inflow_model2):

    prodrisk1 = load_session(plant_name,method1,inflow_model1)
    prodrisk2 = load_session(plant_name,method2,inflow_model2)

    magazines1 = prodrisk1.model.module.get_object_names()
    magazines2 = prodrisk2.model.module.get_object_names()

    total_vol1 = np.zeros_like(prodrisk1.model.module[magazines1[0]].reservoirVolume.get().values)
    total_vol2 = np.zeros_like(prodrisk2.model.module[magazines2[0]].reservoirVolume.get().values)

    for mag1 in magazines1:
        total_vol1 += prodrisk1.model.module[mag1].reservoirVolume.get().values

    for mag2 in magazines2:
        total_vol2 += prodrisk2.model.module[mag2].reservoirVolume.get().values

    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Compare Volume")
    os.makedirs(plot_folder, exist_ok=True)

    index = prodrisk1.model.module[magazines1[0]].reservoirVolume.get().index

    percs = [0,25,50,75,100]
    perc1 = np.percentile(total_vol1,percs,axis=1)
    perc2 = np.percentile(total_vol2,percs,axis=1)

    diff = total_vol2 - total_vol1
    diff_perc = perc2 - perc1

    fig, ax = plt.subplots(figsize=(10,10))

    for p, vals in zip(percs,diff_perc):
        ax.plot(index, vals, label=f"{p}th percentile")
    ax.plot(index,np.mean(diff,axis=1),label="Mean",lw=3,color="black")
    ax.set(title="Difference in Reservoir Volumes", xlabel="Time", ylabel="Volume Difference [Mm$^3$]")
    ax.legend()
    ax.grid()

    path_diff = os.path.join(plot_folder, method1 + "_" + inflow_model1 + "_vs_" + method2 + "_" + inflow_model2 + "_volume_diff.png")
    fig.savefig(path_diff, dpi=300, bbox_inches='tight')

    return 


def compare_volumes_mean(plant_name, method1, method2, inflow_model1, inflow_model2,lim):

    prodrisk1 = load_session(plant_name,method1,inflow_model1)
    prodrisk2 = load_session(plant_name,method2,inflow_model2)

    magazines1 = prodrisk1.model.module.get_object_names()
    magazines2 = prodrisk2.model.module.get_object_names()

    total_vol1 = np.zeros_like(prodrisk1.model.module[magazines1[0]].reservoirVolume.get().values)
    total_vol2 = np.zeros_like(prodrisk2.model.module[magazines2[0]].reservoirVolume.get().values)

    for mag1 in magazines1:
        total_vol1 += prodrisk1.model.module[mag1].reservoirVolume.get().values

    for mag2 in magazines2:
        total_vol2 += prodrisk2.model.module[mag2].reservoirVolume.get().values

    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Compare Volume")
    os.makedirs(plot_folder, exist_ok=True)

    index = prodrisk1.model.module[magazines1[0]].reservoirVolume.get().index


    fig, ax = plt.subplots(figsize=(10,10))
    ax.plot(index,np.mean(total_vol1,axis=1),label=f"{method1}")
    ax.plot(index,np.mean(total_vol2,axis=1),label=f"{method2}")
    ax.set(title=f"Volume means", xlabel="Time", ylabel="Volume [Mm$^3$]",ylim=lim)
    ax.legend(loc="upper left")
    ax.grid()

    path_diff = os.path.join(plot_folder, method1 + "_" + inflow_model1 + "_vs_" + method2 + "_" + inflow_model2 + "_volume_mean.png")
    fig.savefig(path_diff, dpi=300, bbox_inches='tight')

    return 

def compare_three_means(plant_name, method1, inflow_model1, method2, inflow_model2, method3, inflow_model3, lim):

    prodrisk1 = load_session(plant_name,method1,inflow_model1)
    prodrisk2 = load_session(plant_name,method2,inflow_model2)
    prodrisk3 = load_session(plant_name,method3,inflow_model3)

    magazines1 = prodrisk1.model.module.get_object_names()
    magazines2 = prodrisk2.model.module.get_object_names()
    magazines3 = prodrisk3.model.module.get_object_names()

    total_vol1 = np.zeros_like(prodrisk1.model.module[magazines1[0]].reservoirVolume.get().values)
    total_vol2 = np.zeros_like(prodrisk2.model.module[magazines2[0]].reservoirVolume.get().values)
    total_vol3 = np.zeros_like(prodrisk3.model.module[magazines3[0]].reservoirVolume.get().values)

    for mag1 in magazines1:
        total_vol1 += prodrisk1.model.module[mag1].reservoirVolume.get().values

    for mag2 in magazines2:
        total_vol2 += prodrisk2.model.module[mag2].reservoirVolume.get().values

    for mag3 in magazines3:
        total_vol3 += prodrisk3.model.module[mag3].reservoirVolume.get().values

    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Compare Volume")
    os.makedirs(plot_folder, exist_ok=True)

    index = prodrisk1.model.module[magazines1[0]].reservoirVolume.get().index


    fig, ax = plt.subplots(figsize=(10,10))
    ax.plot(index,np.mean(total_vol1,axis=1),label=f"{method1}_{inflow_model1}")
    ax.plot(index,np.mean(total_vol2,axis=1),label=f"{method2}_{inflow_model2}")
    ax.plot(index,np.mean(total_vol3,axis=1),label=f"{method3}_{inflow_model3}")
    ax.set(title=f"Volume means", xlabel="Time", ylabel="Volume [Mm$^3$]",ylim=lim)
    ax.legend(loc="upper left")
    ax.grid()

    path_diff = os.path.join(plot_folder, method1 + "_" + inflow_model1 + "_vs_" + method2 + "_" + inflow_model2 
                             + "_vs_" + method3 + "_" + inflow_model3 + "_volume_mean.png")
    fig.savefig(path_diff, dpi=300, bbox_inches='tight')

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

    fig, axes = plt.subplots(1, len(magazines),figsize=(10,10),sharey=True)

    for i in range(len(magazines)):
        mod = prodrisk.model.module[magazines[i]]
        overflow = mod.overflow.get()
        axes[i].fill_between(overflow.index, np.percentile(overflow.values[:,:],0,axis=1),np.percentile(overflow.values[:,:],100,axis=1),alpha=0.2)
        axes[i].plot(overflow.mean(axis=1))
        axes[i].set(title=magazines[i],xlabel="Time",ylabel="Overflow")
        axes[i].grid()
    fig.suptitle(f"Overflow with {method} and {inflow_model}")

    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Overflow")
    path = os.path.join(plot_folder, method + "_" + inflow_model + "_" + plant_name + "_overflow.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')

    return

def plot_total_overflow(plant_name, method, inflow_model,lim):

    prodrisk = load_session(plant_name,method,inflow_model)

    fig,ax = plt.subplots(figsize=(10,10))

    area = prodrisk.model.area["my_area"]
    tot_overflow = area.total_reservoir_overflow.get()

    # ax.fill_between(tot_overflow.index, np.percentile(tot_overflow.values[:,:],0,axis=1),np.percentile(tot_overflow.values[:,:],100,axis=1),alpha=0.2)
    ax.plot(tot_overflow.mean(axis=1))
    ax.set(title="Total reservoir overflow",xlabel="Time",ylabel="Overflow",ylim=lim)
    ax.grid()

    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Overflow")
    path = os.path.join(plot_folder, method + "_" + inflow_model + "_" + plant_name + "_total_overflow.png")
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
    
    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Inflow")
    path = os.path.join(plot_folder, method + "_" + inflow_model + "_" + plant_name + "_inflow.png")
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
    
    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Discharge")
    path = os.path.join(plot_folder, method + "_" + inflow_model + "_" + plant_name + "_discharge.png")
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
    
    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Production")
    path = os.path.join(plot_folder, method + "_" + inflow_model + "_" + plant_name + "_production.png")
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
    
    plot_folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name,"Results","Bypass")
    path = os.path.join(plot_folder, method + "_" + inflow_model + "_" + plant_name + "_bypass.png")
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

    return [avg_adjusted, cvar10]

def income_serial(plant_name, method, inflow_model):

    prodrisk = load_session(plant_name, method, inflow_model)

    area = prodrisk.model.area["my_area"]

    volume = area.total_reservoir_volume.get().to_numpy()
    production = area.total_production.get().to_numpy()
    price = area.output_price.get().to_numpy()

    # Total revenue over all time periods and scenarios
    total_income = np.sum(production * price)

    # Terminal value of storage
    mean_price = np.mean(price)

    start_value = volume[0, 0] * mean_price
    end_value = volume[-1, -1] * mean_price

    adjusted_income = total_income + end_value - start_value

    return adjusted_income



def obj_value(plant_name,method,inflow_model):

    prodrisk= load_session(plant_name,method,inflow_model)

    area = prodrisk.model.area["my_area"]
    
    objective = area.expected_objective_value.get()

    return objective


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

def water_value_serial(plant_name,method,inflow_model):


    prodrisk = load_session(plant_name, method, inflow_model)

    area = prodrisk.model.area["my_area"]

    water_vals = area.water_value_result.get()

    water_val = water_vals.values[0,0]

    summary_df = pd.DataFrame({
        "First scenario, first week": [water_val]

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




