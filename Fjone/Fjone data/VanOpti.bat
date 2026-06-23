@ECHO OFF
del indvan*.*
del prisrekke.*
copy prisrekke4pNO*.pris prisrekke.pris
ltm < C:\ltm_simulering\skript\klargjor_vassdrag.txt
python C:\temp\shyftrisk\shyftrisk.py FJONE --model_dir . --historical
python C:\temp\shyftrisk\shyftrisk.py FJONE --model_dir . --forecast
python C:\ltm_simulering\skript\update_mean_inflow.py -vassdrag fjone -forste_hele_tilsigsar 1982 -siste_hele_tilsigsar 2018
rem python C:\ltm_simulering\skript\prepare_model.py -forste_hele_tilsigsar 1982 -siste_hele_tilsigsar 2018
ltm < mag.txt
mpiexec -n 22 prodrisk_ms_mpi -SEKV < mag_ProdRisk.txt
rem Kurvetegn res.kurv
rem copy indvan.prd indvan-0.sdv
rem xcopy /E /Y . C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\
copy /Y shop*.dat \\srv0147\Datashare\Kutt\PR10\
rem copy /Y shop*.dat \\172.20.0.63\kraft\marked\Kutt\PR\listenmate\
copy /Y shop*.dat \\srv0147\Datashare\Kutt\PADR10\fjone-18-2022-05-v10.dat
copy /Y *.SDDP C:\ltm_simulering\fjone\ProdRisk_basis
rem Copy DETSIMRES.SIMP \\172.20.0.63\kraft\marked\Kutt\SIMP\DETSIMRES-fjone.SIMP
rem start /B pythonw C:\ltm_simulering\skript\indvan.py indvan.prd -folder C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\ -host srv0087 -port 8086 -db vv -user admin -passwd admin 1>vv.txt 2>&1
rem start /B pythonw C:\ltm_simulering\skript\readDETSIMRES.py DETSIMRES.SIMP -o C:\Kutt\SIMP_TO_CSV\fjone.CSV -op C:\Kutt\SIMP_TO_CSV\fjone-persentil.csv 1>csv.txt 2>&1
rem start /B pythonw C:\ltm_simulering\skript\readSIMP.py C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\ fjone -host srv0087 -port 8086 -db SIMP 1>simp.txt 2>&1
rem start /B pythonw C:\ltm_simulering\skript\readSIMThdf5.py C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\ fjone -host srv0087 -port 8086 -db fjone -user admin -passwd admin 1>simt.txt 2>&1
rem start /B pythonw C:\ltm_simulering\skript\readDYNMODELL.py C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\ fjone -host srv0087 -port 8086 -db fjone -user admin -passwd admin 1>dynmodell.txt 2>&1
rem start /B pythonw C:\ltm_simulering\skript\readSIMThdf5.py C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\ fjone -host srv0087 -port 8086 -db prodrisk_test -user admin -passwd admin -op yes 1>op.txt 2>&1
start /B pythonw C:\ltm_simulering\skript\indvan.py indvan.prd -folder C:\LTM_simulering\fjone\18-2022-05-v10-prodrisk\ -host influx -port 8086 -db vv  -user prodrisk -passwd 1R3KzJR8NuCQ2W8!sNp!j 1>vv_vminflux.txt 2>&1
start /B pythonw C:\ltm_simulering\skript\readDYNMODELL.py C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\ fjone -host influx -port 8086 -db fjone -user prodrisk -passwd 1R3KzJR8NuCQ2W8!sNp!j 1>dynmodell.txt 2>&1
start /B pythonw C:\ltm_simulering\skript\readSIMThdf5.py C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\ fjone -host influx -port 8086 -db operasjonell -user prodrisk -passwd 1R3KzJR8NuCQ2W8!sNp!j -op yes 1>op_new.txt 2>&1
start /B pythonw C:\ltm_simulering\skript\readSIMThdf5.py C:\ltm_simulering\fjone\18-2022-05-v10-prodrisk\ fjone -host influx -port 8086 -db fjone -user prodrisk -passwd 1R3KzJR8NuCQ2W8!sNp!j 1>simt_new.txt 2>&1
