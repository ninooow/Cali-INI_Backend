import time
from fastapi.testclient import TestClient
from fastapi_app import app

client = TestClient(app)

print("Executing POST /api/v1/analytics/runs...")
start_time = time.time()
response = client.post("/api/v1/analytics/runs")
end_time = time.time()

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
print(f"Time taken: {end_time - start_time:.2f} seconds")

if response.status_code not in [200, 201]:
    print("Execution failed.")
    exit(1)

run_id = response.json()["run_id"]
status = response.json()["status"]

print(f"run_id: {run_id}, status: {status}")

cond_resp = client.get(f"/api/v1/analytics/condition-inferences?run_id={run_id}")
cond_count = len(cond_resp.json()["data"])

forecast_resp = client.get(f"/api/v1/analytics/parameter-forecasts?run_id={run_id}")
forecast_count = len(forecast_resp.json()["data"])

rca_resp = client.get(f"/api/v1/analytics/rca-matches?run_id={run_id}")
rca_count = len(rca_resp.json()["data"])

print(f"RESULT: run_id={run_id}, status={status}, condition_count={cond_count}, forecast_count={forecast_count}, rca_count={rca_count}")
