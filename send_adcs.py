import csv
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

url = "http://127.0.0.1:5002/api/adcs/live"
csv_path = Path(__file__).with_name("aurora1_angle_telemetry.csv")

with csv_path.open(newline="", encoding="utf-8") as file:
    start = time.monotonic()
    for row in csv.DictReader(file):
        time_s = float(row["time_s"])
        angle_deg = float(row["actual_angle_deg"])

        # Wait until this sample is due, accounting for time spent sending.
        time.sleep(max(0, start + time_s - time.monotonic()))

        packet = {"time_s": time_s, "actual_angle_deg": angle_deg}
        request = Request(
            url,
            data=json.dumps(packet).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=3) as response:
            print(f"{response.status} | {time_s:5.2f} s | {angle_deg:6.2f}°")