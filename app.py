from flask import Flask, render_template
import random
from datetime import datetime

app = Flask(__name__)

event_log = []


def add_event(message, event_type="INFO"):
    event = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": message,
        "type": event_type
    }

    event_log.insert(0, event)

    if len(event_log) > 8:
        event_log.pop()


def check_subsystems(battery, temperature):
    subsystems = {
        "EPS": "Nominal",
        "ADCS": "Nominal",
        "COMMS": "Nominal",
        "OBC": "Nominal"
    }

    if battery < 75:
        subsystems["EPS"] = "Warning"
        add_event("EPS warning — battery below threshold", "WARNING")

    if temperature > 32:
        subsystems["OBC"] = "Warning"
        add_event("OBC warning — high temperature", "WARNING")

    if random.randint(1, 10) == 1:
        subsystems["COMMS"] = "Warning"
        add_event("COMMS warning — simulated signal fault", "WARNING")

    if random.randint(1, 12) == 1:
        subsystems["ADCS"] = "Warning"
        add_event("ADCS warning — attitude fault detected", "WARNING")

    return subsystems


@app.route("/")
def home():
    battery = random.randint(70, 100)
    temperature = random.randint(18, 35)
    altitude = random.randint(400, 425)
    mode = random.choice(["Science", "Communication", "Standby"])

    if battery < 75:
        status = "Low Battery"
    elif temperature > 32:
        status = "Thermal Warning"
    else:
        status = "Nominal"

    telemetry = {
        "battery": battery,
        "temperature": temperature,
        "altitude": altitude,
        "mode": mode,
        "status": status
    }

    subsystems = check_subsystems(battery, temperature)

    add_event("Telemetry packet received")

    return render_template(
        "index.html",
        telemetry=telemetry,
        subsystems=subsystems,
        event_log=event_log
    )


if __name__ == "__main__":
    app.run(debug=True)