@echo off

cd ../..

rd /S /Q Server
xcopy ObjectsDetection\Server Server /I /E
xcopy ObjectsDetection\ObjectsUnification Server\ObjectsUnification /I /E
xcopy ObjectsDetection\ImageProcessing Server\ImageProcessing /I /E
xcopy ObjectsDetection\DataModel Server\DataModel /I /E
xcopy ObjectsDetection\Common Server\Common /I /E

echo cd C:\Users\Kamil\Dysk Google\UCZELNIA\Praca inzynierska > run_server.bat
echo cd Server ^& start python run.py >> run_server.bat

mkdir Logs

echo DONE
pause