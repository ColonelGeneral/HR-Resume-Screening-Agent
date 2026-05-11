import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"
TEST_DATA_DIR = "test_data"

print("\n" + "="*60)
print("HR SHORTLISTING AGENT - MULTI-JD TEST REPORT")
print("="*60 + "\n")

# Test 1: Senior Data Scientist
print("[TEST 1] Senior Data Scientist JD")
print("-" * 60)
try:
    with open(f"{TEST_DATA_DIR}/senior_data_scientist_jd.txt", "rb") as f:
        files = {"file": f}
        data = {"role_title": "Senior Data Scientist"}
        response = requests.post(f"{BASE_URL}/jobs/upload", files=files, data=data)
    
    jd1 = response.json()
    job_id_1 = jd1["job_id"]
    print(f"✓ Job ID: {job_id_1}")
    print(f"  Role: {jd1['role_title']}")
    print(f"  Skills: {', '.join(jd1['required_skills'][:5])}")
    print(f"  Experience: {jd1['experience_years']}+ years\n")
    
    # Evaluate
    eval_data = {"job_id": job_id_1, "candidate_ids": None}
    eval_response = requests.post(f"{BASE_URL}/evaluate", json=eval_data)
    rankings_1 = eval_response.json()["rankings"]
    
    print("  RANKINGS:")
    for r in rankings_1:
        rec_icon = "✓" if r["recommendation"] == "Hire" else "~" if r["recommendation"] == "Review" else "✗"
        print(f"  {rec_icon} {r['candidate_name']}: {r['total_score']:.2f} pts | {r['recommendation']} | Confidence: {r['confidence']:.2f}")
    print()
    
except Exception as e:
    print(f"✗ Error in Test 1: {e}\n")

# Test 2: Junior Frontend
print("[TEST 2] Junior Frontend Developer JD")
print("-" * 60)
try:
    with open(f"{TEST_DATA_DIR}/junior_frontend_jd.txt", "rb") as f:
        files = {"file": f}
        data = {"role_title": "Junior Frontend Developer"}
        response = requests.post(f"{BASE_URL}/jobs/upload", files=files, data=data)
    
    jd2 = response.json()
    job_id_2 = jd2["job_id"]
    print(f"✓ Job ID: {job_id_2}")
    print(f"  Role: {jd2['role_title']}")
    print(f"  Skills: {', '.join(jd2['required_skills'][:5])}")
    print(f"  Experience: {jd2['experience_years']}+ years\n")
    
    # Evaluate
    eval_data = {"job_id": job_id_2, "candidate_ids": None}
    eval_response = requests.post(f"{BASE_URL}/evaluate", json=eval_data)
    rankings_2 = eval_response.json()["rankings"]
    
    print("  RANKINGS:")
    for r in rankings_2:
        rec_icon = "✓" if r["recommendation"] == "Hire" else "~" if r["recommendation"] == "Review" else "✗"
        print(f"  {rec_icon} {r['candidate_name']}: {r['total_score']:.2f} pts | {r['recommendation']} | Confidence: {r['confidence']:.2f}")
    print()
    
except Exception as e:
    print(f"✗ Error in Test 2: {e}\n")

# Test 3: Full Stack Engineer
print("[TEST 3] Full Stack Engineer JD")
print("-" * 60)
try:
    with open(f"{TEST_DATA_DIR}/fullstack_engineer_jd.txt", "rb") as f:
        files = {"file": f}
        data = {"role_title": "Full Stack Engineer"}
        response = requests.post(f"{BASE_URL}/jobs/upload", files=files, data=data)
    
    jd3 = response.json()
    job_id_3 = jd3["job_id"]
    print(f"✓ Job ID: {job_id_3}")
    print(f"  Role: {jd3['role_title']}")
    print(f"  Skills: {', '.join(jd3['required_skills'][:5])}")
    print(f"  Experience: {jd3['experience_years']}+ years\n")
    
    # Evaluate
    eval_data = {"job_id": job_id_3, "candidate_ids": None}
    eval_response = requests.post(f"{BASE_URL}/evaluate", json=eval_data)
    rankings_3 = eval_response.json()["rankings"]
    
    print("  RANKINGS:")
    for r in rankings_3:
        rec_icon = "✓" if r["recommendation"] == "Hire" else "~" if r["recommendation"] == "Review" else "✗"
        print(f"  {rec_icon} {r['candidate_name']}: {r['total_score']:.2f} pts | {r['recommendation']} | Confidence: {r['confidence']:.2f}")
    print()
    
except Exception as e:
    print(f"✗ Error in Test 3: {e}\n")

# Summary Comparison Table
print("\n" + "="*60)
print("SUMMARY COMPARISON TABLE")
print("="*60 + "\n")

try:
    # Collect all scores
    scores = {}
    for r in rankings_1:
        if r["candidate_name"] not in scores:
            scores[r["candidate_name"]] = {}
        scores[r["candidate_name"]]["Senior DS"] = r["total_score"]
    
    for r in rankings_2:
        if r["candidate_name"] not in scores:
            scores[r["candidate_name"]] = {}
        scores[r["candidate_name"]]["Junior FE"] = r["total_score"]
    
    for r in rankings_3:
        if r["candidate_name"] not in scores:
            scores[r["candidate_name"]] = {}
        scores[r["candidate_name"]]["Full Stack"] = r["total_score"]
    
    # Print table
    print(f"{'Candidate':<20} {'Senior DS':<15} {'Junior FE':<15} {'Full Stack':<15}")
    print("-" * 65)
    for candidate, jd_scores in sorted(scores.items()):
        ds_score = f"{jd_scores.get('Senior DS', 0):.2f}" if "Senior DS" in jd_scores else "N/A"
        fe_score = f"{jd_scores.get('Junior FE', 0):.2f}" if "Junior FE" in jd_scores else "N/A"
        fs_score = f"{jd_scores.get('Full Stack', 0):.2f}" if "Full Stack" in jd_scores else "N/A"
        print(f"{candidate:<20} {ds_score:<15} {fe_score:<15} {fs_score:<15}")
    
except Exception as e:
    print(f"Error creating summary: {e}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60 + "\n")
