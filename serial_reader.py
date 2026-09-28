import time
import serial

PORT = "/dev/cu.usbmodem90706925BDF42"
BAUD_RATE = 9600

arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)

print("AURORA-1 Arduino connected!")

try:
    while True:
        reading = arduino.readline().decode("utf-8").strip()

        if reading:
            print(f"AURORA-1 sensor: {reading}")

except KeyboardInterrupt:
    print("\nConnection closed.")

finally:
    arduino.close()