@echo off

for /f "tokens=1,2 delims==" %%a in (RaspberryScripts/raspberry_params.txt) do (
	
	IF "%%a"=="ip" ( SET "raspberry_ip=%%b" )
	IF "%%a"=="user" ( SET "raspberry_user=%%b" )
	IF "%%a"=="password" ( SET "raspberry_password=%%b" )
)



cd ..
7z a deploy.zip Agent
7z a deploy.zip Common
7z a deploy.zip DataModel

pscp -pw %raspberry_password% deploy.zip %raspberry_user%@%raspberry_ip%:ObjectsDetection.zip

del deploy.zip

cd Deploy
plink -ssh %raspberry_user%@%raspberry_ip% -pw %raspberry_password% -m RaspberryScripts/raspberry_deploy_script.txt

echo DONE