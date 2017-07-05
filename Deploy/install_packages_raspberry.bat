@echo off

for /f "tokens=1,2 delims==" %%a in (raspberry_params.txt) do (
	
	IF "%%a"=="ip" ( SET "raspberry_ip=%%b" )
	IF "%%a"=="user" ( SET "raspberry_user=%%b" )
	IF "%%a"=="password" ( SET "raspberry_password=%%b" )
)



plink -ssh %raspberry_user%@%raspberry_ip% -pw %raspberry_password% -m raspberry_packages_list.txt

echo DONE
pause