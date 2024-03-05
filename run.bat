@echo off

set python_executable=C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe

echo Starting authentication server...
start "" /B %python_executable% "Kerberos_project\auth server\server.py"
timeout /t 2 >nul

echo Starting message server...
start "" /B %python_executable% "Kerberos_project\msg server\msg new.py"
timeout /t 2 >nul

echo Starting client...
start "" /B %python_executable% "Kerberos_project\client\client.py"

pause