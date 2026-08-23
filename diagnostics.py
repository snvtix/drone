import time
import socket
import ps_drone

def check_port(ip, port, timeout=1.0):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

def print_state_bits(state):
    labels = [
        "FLYING", "VIDEO", "VISION", "CONTROL", "ALTITUDE",
        "USER_FEEDBACK", "ACK", "CAMERA_READY",
        "TRAVELLING", "USB_READY", "NAVDATA_DEMO", "BOOTSTRAP",
        "MOTORS_PROBLEM", "COM_LOST", "SOFTWARE_FAULT", "VBAT_LOW",
        "USER_EL", "TIMER_ELAPSED", "MAGNETO_NEEDS_CALIB",
        "ANGLES_OUT_OF_RANGE", "WIND", "ULTRASOUND", "CUTOUT",
        "PIC_VERSION_OK", "ATCODEC_THREAD", "NAVDATA_THREAD",
        "VIDEO_THREAD", "ACQ_THREAD", "CTRL_WATCHDOG",
        "ADC_WATCHDOG", "COM_WATCHDOG", "EMERGENCY"
    ]
    print("\n=== STATE BITS ===")
    for i, bit in enumerate(state[:32]):
        print(f"{i:02d} {labels[i]:25s}: {bit}")

def diagnostic():
    drone = ps_drone.Drone()
    print("\n=== STARTING DRONE DIAGNOSTICS ===")

    print("\n[1] Checking Wi‑Fi connection...")
    if not check_port("192.168.1.1", 23):
        print("❌ Drone unreachable — Wi‑Fi not connected")
        return
    print("✔ Wi‑Fi OK")

    print("\n[2] Starting PS‑Drone...")
    drone.startup()

    print("\n[3] Resetting emergency state...")
    drone.reset()
    while drone.getBattery()[0] == -1:
        time.sleep(0.1)
    time.sleep(0.5)

    print("\n[4] Battery status:")
    bat = drone.getBattery()
    print(f"   ✔ Battery: {bat[0]}% ({bat[1]})")

    print("\n[5] Checking NavData availability...")
    if drone.NavDataCount == 0:
        print("❌ No NavData received — sensors offline")
    else:
        print("✔ NavData OK")

    print("\n[6] Checking system state bits...")
    print_state_bits(drone.State)

    print("\n[7] Checking camera readiness...")
    if drone.State[7] == 1:
        print("✔ Camera ready")
    else:
        print("❌ Camera not ready")

    print("\n[8] Checking emergency state...")
    if drone.State[31] == 1:
        print("❌ DRONE IN EMERGENCY — must reset before takeoff")
    else:
        print("✔ No emergency")

    print("\n[9] Checking IMU calibration...")
    if drone.State[19] == 1:
        print("❌ Angles out of range — drone not level")
    else:
        print("✔ IMU OK")

    print("\n[10] Checking motor status...")
    if drone.State[12] == 1:
        print("❌ Motor problem detected")
    else:
        print("✔ Motors OK")

    print("\n[11] Checking communication watchdog...")
    if drone.State[30] == 1:
        print("❌ Communication watchdog triggered — unstable link")
    else:
        print("✔ Communication OK")

    print("\n=== SUMMARY ===")
    ready = True

    if drone.State[31] == 1:
        print("❌ EMERGENCY active")
        ready = False
    if drone.State[19] == 1:
        print("❌ Drone not level (IMU)")
        ready = False
    if drone.State[12] == 1:
        print("❌ Motor error")
        ready = False
    if bat[0] < 12:
        print("❌ Battery too low for takeoff")
        ready = False

    if ready:
        print("\n✔ DRONE IS READY FOR TAKEOFF")
    else:
        print("\n⚠ DRONE IS *NOT* READY FOR TAKEOFF — see errors above")

if __name__ == "__main__":
    diagnostic()
