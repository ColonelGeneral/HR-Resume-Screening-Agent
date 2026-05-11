# HR Shortlisting Full Workflow Test

$BASE_URL = "http://127.0.0.1:8000"
$JD_FILE = "test_data/job_description.txt"
$RESUME_FILES = @("test_data/resume_john.txt", "test_data/resume_sarah.txt", "test_data/resume_michael.txt")

Write-Host "=== HR SHORTLISTING WORKFLOW TEST ===" -ForegroundColor Cyan

# Step 1: Upload Job Description
Write-Host "`n[1] Uploading Job Description..." -ForegroundColor Yellow
$jd_form = @{
    file = Get-Item $JD_FILE
    role_title = "Senior AI Engineer"
}
$jd_response = Invoke-RestMethod -Uri "$BASE_URL/jobs/upload" -Method Post -Form $jd_form
$job_id = $jd_response.job_id
Write-Host "Job Description uploaded (ID: $job_id)" -ForegroundColor Green
Write-Host "  Role: $($jd_response.role_title)"
Write-Host "  Required Skills: $($jd_response.required_skills -join ', ')"
Write-Host "  Experience: $($jd_response.experience_years) years"

# Step 2: Upload Resumes
Write-Host "`n[2] Uploading Resumes..." -ForegroundColor Yellow
$resume_files_obj = @()
foreach ($file in $RESUME_FILES) {
    $resume_files_obj += Get-Item $file
}
$upload_form = @{
    files = $resume_files_obj
}
$upload_response = Invoke-RestMethod -Uri "$BASE_URL/candidates/upload" -Method Post -Form $upload_form
Write-Host "Resumes uploaded:" -ForegroundColor Green
foreach ($record in $upload_response.records) {
    if ($record.candidate_id) {
        Write-Host "  - ID: $($record.candidate_id) | Name: $($record.name)"
    } else {
        Write-Host "  - Error: $($record.error)"
    }
}

# Step 3: Run Evaluation
Write-Host "`n[3] Running Evaluation..." -ForegroundColor Yellow
$eval_body = @{
    job_id = $job_id
    candidate_ids = $null
} | ConvertTo-Json
$eval_response = Invoke-RestMethod -Uri "$BASE_URL/evaluate" -Method Post -Body $eval_body -ContentType "application/json"
Write-Host "Evaluation completed" -ForegroundColor Green
Write-Host "  Candidates evaluated: $($eval_response.rankings.Count)"

# Step 4: Display Rankings
Write-Host "`n[4] CANDIDATE RANKINGS:" -ForegroundColor Yellow
$eval_response.rankings | ForEach-Object {
    $rank = $eval_response.rankings.IndexOf($_) + 1
    Write-Host "`nRank $rank : $($_.candidate_name)"
    Write-Host "  Score: $($_.total_score) | Confidence: $([math]::Round($_.confidence, 2))"
    Write-Host "  Recommendation: $($_.recommendation)"
}

Write-Host "`n=== TEST COMPLETE ===" -ForegroundColor Cyan
