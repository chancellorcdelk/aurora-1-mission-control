from flask import Flask, render_template, request, redirect, url_for
import random
from datetime import datetime

app = Flask(__name__)

mission_start = datetime.now()

event_log = []
telemetry_history = []

current_mode = "Science"


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
        add_event(
            "EPS warning — battery below threshold",
            "WARNING"
        )

    if temperature > 32:
        subsystems["OBC"] = "Warning"
        add_event(
            "OBC warning — high temperature",
            "WARNING"
        )

    if random.randint(1, 10) == 1:
        subsystems["COMMS"] = "Warning"
        add_event(
            "COMMS warning — simulated signal fault",
            "WARNING"
        )

    if random.randint(1, 12) == 1:
        subsystems["ADCS"] = "Warning"
        add_event(
            "ADCS warning — attitude fault detected",
            "WARNING"
        )

    return subsystems


@app.route("/")
def home():
    battery = random.randint(70, 100)
    temperature = random.randint(18, 35)
    altitude = random.randint(400, 425)

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
        "mode": current_mode,
        "status": status
    }

    subsystems = check_subsystems(
        battery,
        temperature
    )

    telemetry_history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "battery": battery,
        "temperature": temperature,
        "altitude": altitude
    })

    if len(telemetry_history) > 20:
        telemetry_history.pop(0)

    add_event("Telemetry packet received")

    elapsed = datetime.now() - mission_start

    total_seconds = int(elapsed.total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    mission_time = f"{hours:02}:{minutes:02}:{seconds:02}"

    return render_template(
        "index.html",
        telemetry=telemetry,
        subsystems=subsystems,
        event_log=event_log,
        history=telemetry_history,
        mission_time=mission_time,
        current_mode=current_mode
    )


@app.route("/control", methods=["POST"])
def control():
    global current_mode

    new_mode = request.form.get("mode")

    if new_mode in ["Science", "Communication", "Standby"]:
        current_mode = new_mode

        add_event(
            f"Command accepted — switched to {new_mode} mode",
            "COMMAND"
        )

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)