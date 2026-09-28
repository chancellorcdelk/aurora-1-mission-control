from flask import Flask, render_template, request, redirect, url_for
import random
import serial
import threading
import time
from datetime import datetime

app = Flask(__name__)

mission_start = datetime.now()

event_log = []
telemetry_history = []

current_mode = "Science"

sensor_value = None
arduino_connected = False

ARDUINO_PORT = "/dev/cu.usbmodem90706925BDF42"
BAUD_RATE = 9600


def add_event(message, event_type="INFO"):
    event = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": message,
        "type": event_type
    }

    event_log.insert(0, event)

    if len(event_log) > 8:
        event_log.pop()


def read_arduino():
    global sensor_value, arduino_connected

    disconnect_reported = False

    while True:
        try:
            with serial.Serial(
                ARDUINO_PORT,
                BAUD_RATE,
                timeout=1
            ) as arduino:
                time.sleep(2)

                arduino_connected = True
                disconnect_reported = False

                add_event(
                    "Arduino hardware telemetry link established"
                )

                while True:
                    reading = (
                        arduino.readline()
                        .decode("utf-8")
                        .strip()
                    )

                    if reading:
                        sensor_value = int(reading)

        except (serial.SerialException, OSError, ValueError):
            arduino_connected = False
            sensor_value = None

            if not disconnect_reported:
                add_event(
                    "Arduino telemetry link unavailable",
                    "WARNING"
                )
                disconnect_reported = True

            time.sleep(2)


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
            "OBC warning — hardware temperature above threshold",
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
    altitude = random.randint(400, 425)

    if sensor_value is not None:
        temperature = round(
            20 + (sensor_value / 1023) * 24,
            1
        )
        telemetry_source = "Arduino Hardware"
    else:
        temperature = random.randint(18, 35)
        telemetry_source = "Simulation"

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
        "status": status,
        "sensor_value": sensor_value,
        "source": telemetry_source,
        "arduino_connected": arduino_connected
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

    add_event(
        f"Telemetry packet received from {telemetry_source}"
    )

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

    if new_mode in [
        "Science",
        "Communication",
        "Standby"
    ]:
        current_mode = new_mode

        add_event(
            f"Command accepted — switched to {new_mode} mode",
            "COMMAND"
        )

    return redirect(url_for("home"))


if __name__ == "__main__":
    arduino_thread = threading.Thread(
        target=read_arduino,
        daemon=True
    )
    arduino_thread.start()

    app.run(
        debug=True,
        use_reloader=False
    )