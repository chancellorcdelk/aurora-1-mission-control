from flask import Flask, render_template
import random

app = Flask(__name__)

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

    return render_template("index.html", telemetry=telemetry)

if __name__ == "__main__":
    app.run(debug=True)