import cv2
from windowcapture import WindowCapture
from time import time, sleep
import pyautogui

# TrackerBoosting
# TrackerKCF
# TrackerCSRT (best)
# TrackerMedianFlow
# TrackerMOSSE
# TrackerMIL
# TrackerTLD
tracker = cv2.legacy.TrackerCSRT().create()

wincap = WindowCapture("Minecraft* 1.20.1 - Singleplayer")
screenshot = wincap.get_screenshot()

bbox_init = cv2.selectROI(screenshot)
y_init = bbox_init[1]

ok = tracker.init(screenshot, bbox_init)

loop_time = time()
while(True):
    frame = wincap.get_screenshot()

    ok, bbox = tracker.update(frame)

    if y_init - bbox[1] <= -20:
        pyautogui.click(button='right')
        sleep(1)
        pyautogui.click(button='right')
        sleep(2)
        continue
    if y_init - bbox[1] >= 50:
        pyautogui.click(button='right')
        sleep(1)
        pyautogui.click(button='right')
        sleep(2)

        del tracker
        tracker = cv2.legacy.TrackerCSRT().create()

        frame = wincap.get_screenshot()
        ok = tracker.init(frame, bbox_init)

    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)
        cv2.putText(frame, str(1 / (time() - loop_time)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "Error!", (0, 0), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)

    cv2.imshow('Computer Vision', frame)

    loop_time = time()

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
