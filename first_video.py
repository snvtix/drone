#########
# firstVideo.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows the general usage of the video-function of a Parrot AR.Drone 2.0 using the PS-Drone-API.
# The drone will stay on the ground.
# Dependencies: a POSIX OS, openCV2, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time
import ps_drone
import multiprocessing

def main():

    drone = ps_drone.Drone()

    drone.debug = True
    drone.showCommands = True

    drone.startup()
    drone.reset()
    
    print("CONFIG:")
    drone.getConfig()

    time.sleep(2)

    for x in drone.ConfigData:
        if "version" in x[0].lower():
            print(x)

    while drone.getBattery()[0] == -1:
        time.sleep(0.1)

    print("Battery:", drone.getBattery())

    drone.useDemoMode(True)

    drone.setConfigAllID()

    drone.sdVideo()
    drone.frontCam()

    print("\nCzekam 5 sekund na konfigurację...\n")
    time.sleep(5)

    print("\n=== VIDEO CONFIG ===")

    for item in drone.ConfigData:
        try:
            if "video" in item[0].lower():
                print(item)
        except:
            pass

    print("\n=== DRONE STATE ===")
    print("Camera Mask :", drone.State[7])
    print("Video Thread:", drone.State[26])

    print("\n=== START VIDEO ===")

    drone.startVideo()
    drone.getNDpackage(["video_stream"])
    
    print("\n=== PROCESY ===")
    
    for p in multiprocessing.active_children():
        print(p)

    for i in range(20):

        print(
            f"{i:02d}",
            "Camera =", drone.State[7],
            "Video =", drone.State[26],
            "Ready =", drone.VideoReady,
            "Count =", drone.VideoImageCount
        )
        print(drone.NavData.keys())

        time.sleep(1)

    drone.stopVideo()
    drone.shutdown()


if __name__ == "__main__":
    main()
