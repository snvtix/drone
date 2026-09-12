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
import time, sys
import ps_drone
import cv2

drone = ps_drone.Drone()
drone.startup()

drone.reset()
while drone.getBattery()[0] == -1:
    time.sleep(0.1)

print("Battery: " + str(drone.getBattery()[0]) + "%  " + str(drone.getBattery()[1]))

drone.useDemoMode(True)
drone.setConfigAllID()
drone.sdVideo()
drone.frontCam()

CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:
    time.sleep(0.0001)

drone.startVideo()

print("Nacisnij 'q' w oknie wideo, aby zakonczyc.")
while True:
    img = drone.getImage() # Pobranie surowej klatki bezpośrednio z drona
    if img is not None:
        cv2.imshow("AR.Drone Video", img)
        
    # Sterowanie i zamknięcie przez okno OpenCV
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        # Przełączanie kamery
        ground = not getattr(drone, 'ground_state', False)
        drone.ground_state = ground
        drone.groundVideo(ground)

cv2.destroyAllWindows()
drone.stopVideo()
