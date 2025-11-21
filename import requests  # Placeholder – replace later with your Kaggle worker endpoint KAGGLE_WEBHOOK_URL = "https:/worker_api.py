import requests

# Placeholder – replace later with your Kaggle worker endpoint
KAGGLE_WEBHOOK_URL = "https://your-kaggle-worker-url"

def notify_kaggle_worker(job_id):
    try:
        requests.post(KAGGLE_WEBHOOK_URL, data={"job_id": job_id})
        print("Kaggle worker notified:", job_id)
    except Exception as e:
        print("Kaggle notify failed:", e)
