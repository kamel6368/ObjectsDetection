@echo off

SET raspberry_ip=192.168.1.6
SET raspberry_user=pi
SET raspberry_password=raspberry

cd ..
7z a deploy.zip Agent
7z a deploy.zip Common

pscp -pw %raspberry_password% deploy.zip pi@%raspberry_ip%:ObjectsDetection.zip

del deploy.zip

cd Deploy
putty -ssh %raspberry_user%@%raspberry_ip% -pw %raspberry_password% -m raspberry_script.txt

echo DONE