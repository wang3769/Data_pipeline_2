import schedule
import time
from pipeline import run_pipeline

def job():
    run_pipeline("AAPL", "2016-01-01", "2025-01-01")

schedule.every().day.at("17:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
