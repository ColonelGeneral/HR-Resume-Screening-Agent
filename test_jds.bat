@echo off
setlocal enabledelayedexpansion

echo ========================================
echo HR SHORTLISTING - MULTI-JD TEST REPORT
echo ========================================
echo.
echo Starting tests...
echo.

set BASE_URL=http://127.0.0.1:8000

REM Wait for server to be ready
timeout /t 2 /nobreak

echo.
echo [TEST 1] Senior Data Scientist JD
echo ==================================
curl.exe -X POST -F "file=@test_data/senior_data_scientist_jd.txt" -F "role_title=Senior Data Scientist" %BASE_URL%/jobs/upload 2>nul > test_results_1.json
echo Uploaded JD, extracting job_id...
for /f "tokens=*" %%A in (test_results_1.json) do (
    echo %%A
    REM Parse job_id using powershell
)
echo.

echo [Evaluating candidates against Senior Data Scientist role...]
REM Read the job_id and prepare evaluation request
powershell -Command "$json = Get-Content test_results_1.json | ConvertFrom-Json; $job_id = $json.job_id; $eval = @{job_id=$job_id;candidate_ids=$null} | ConvertTo-Json; Write-Host 'Job ID: '$job_id; $eval | Out-File eval_1.json -Encoding ASCII"

curl.exe -X POST -H "Content-Type: application/json" -d @eval_1.json %BASE_URL%/evaluate 2>nul > eval_results_1.json
echo.
echo RANKINGS:
powershell -Command "$json = Get-Content eval_results_1.json | ConvertFrom-Json; $json.rankings | ForEach-Object { Write-Host $_.candidate_name ' - Score: ' $_.total_score ' - Rec: ' $_.recommendation }"
echo.
echo.

echo [TEST 2] Junior Frontend Developer JD
echo ====================================
curl.exe -X POST -F "file=@test_data/junior_frontend_jd.txt" -F "role_title=Junior Frontend Developer" %BASE_URL%/jobs/upload 2>nul > test_results_2.json
echo Uploaded JD, extracting job_id...
echo.

echo [Evaluating candidates against Junior Frontend role...]
powershell -Command "$json = Get-Content test_results_2.json | ConvertFrom-Json; $job_id = $json.job_id; $eval = @{job_id=$job_id;candidate_ids=$null} | ConvertTo-Json; Write-Host 'Job ID: '$job_id; $eval | Out-File eval_2.json -Encoding ASCII"

curl.exe -X POST -H "Content-Type: application/json" -d @eval_2.json %BASE_URL%/evaluate 2>nul > eval_results_2.json
echo.
echo RANKINGS:
powershell -Command "$json = Get-Content eval_results_2.json | ConvertFrom-Json; $json.rankings | ForEach-Object { Write-Host $_.candidate_name ' - Score: ' $_.total_score ' - Rec: ' $_.recommendation }"
echo.
echo.

echo [TEST 3] Full Stack Engineer JD
echo =============================
curl.exe -X POST -F "file=@test_data/fullstack_engineer_jd.txt" -F "role_title=Full Stack Engineer" %BASE_URL%/jobs/upload 2>nul > test_results_3.json
echo Uploaded JD, extracting job_id...
echo.

echo [Evaluating candidates against Full Stack Engineer role...]
powershell -Command "$json = Get-Content test_results_3.json | ConvertFrom-Json; $job_id = $json.job_id; $eval = @{job_id=$job_id;candidate_ids=$null} | ConvertTo-Json; Write-Host 'Job ID: '$job_id; $eval | Out-File eval_3.json -Encoding ASCII"

curl.exe -X POST -H "Content-Type: application/json" -d @eval_3.json %BASE_URL%/evaluate 2>nul > eval_results_3.json
echo.
echo RANKINGS:
powershell -Command "$json = Get-Content eval_results_3.json | ConvertFrom-Json; $json.rankings | ForEach-Object { Write-Host $_.candidate_name ' - Score: ' $_.total_score ' - Rec: ' $_.recommendation }"
echo.
echo.

echo ========================================
echo TEST COMPLETE - Results saved to:
echo test_results_1.json (JD1)
echo test_results_2.json (JD2)
echo test_results_3.json (JD3)
echo eval_results_1.json (Rankings for Test 1)
echo eval_results_2.json (Rankings for Test 2)
echo eval_results_3.json (Rankings for Test 3)
echo ========================================
