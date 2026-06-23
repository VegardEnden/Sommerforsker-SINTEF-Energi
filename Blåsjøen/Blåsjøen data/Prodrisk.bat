echo Off
::INITIALISERING
set PATHINFO=\\oslwpltm001p\Production\HPCRuntime
if %COMPUTERNAME% == OSLWPLTM002P set PATHINFO=\\oslwpltm001p\Production\HPCRuntime
if %COMPUTERNAME% == OSLWPLTM001P set PATHINFO=\\oslwpltm001p\Production\HPCRuntime
if %COMPUTERNAME% == VIEWPLTM002P set PATHINFO=\\viewpltm001p\Preproduction\HPCRuntime


echo *** Prodrisk starter ***
time /t
powershell -file Prodrisk.ps1
echo Off

echo *** Prodrisk ferdig***
	time /t

echo Off