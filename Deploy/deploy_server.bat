@echo off

cd ../..

rd /S /Q ObjectsDetectionApp
xcopy ObjectsDetection\Server ObjectsDetectionApp /I /E
xcopy ObjectsDetection\ObjectsUnification ObjectsDetectionApp\ObjectsUnification /I /E
xcopy ObjectsDetection\ImageProcessing ObjectsDetectionApp\ImageProcessing /I /E
xcopy ObjectsDetection\DataModel ObjectsDetectionApp\DataModel /I /E
xcopy ObjectsDetection\Common ObjectsDetectionApp\Common /I /E

echo cd C:\Users\Kamil\Dysk Google\UCZELNIA\Praca inzynierska > run_server.bat
echo cd ObjectsDetectionApp ^& start python run.py >> run_server.bat

mkdir Logs

echo DONE
