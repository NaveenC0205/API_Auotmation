@echo off
echo Running API Test Suite...

:: Set the Python executable path (modify this if needed)
set PYTHON_EXECUTABLE=python

:: Set the script path dynamically
set SCRIPT_PATH="C:\Users\Naveen\pythonProject\pythonProject\Assignment\edda29879786e996d997e8963c7c2435\E2E_Framework\Tsuites\api_suite.py"

:: Execute the script and log output
%PYTHON_EXECUTABLE% %SCRIPT_PATH% > "C:\Users\Naveen\pythonProject\pythonProject\Assignment\edda29879786e996d997e8963c7c2435\E2E_Framework\Tsuites\api_suite_log.txt" 2>&1

:: Check exit status
if %ERRORLEVEL% NEQ 0 (
    echo API Test Suite Execution Failed! Check api_suite_log.txt for details.
) else (
    echo API Test Suite Execution Completed Successfully.
)

:: Pause the script to see output
pause

