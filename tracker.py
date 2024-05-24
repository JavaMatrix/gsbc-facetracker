import cv2
import matplotlib.pyplot as plt
from time import sleep

# Pixels per second, adjust as needed
CAMERA_SPEED = 10

# Pixels tolerance before moving camera, adjust as needed
DEADZONE = 0

# I think this is different for webcams vs actual cameras, adjust as needed
MIRROR = True

# Change this depending on serial info
OUTPUTS = ["/dev/ttyACM", "./out.log"]

# Seconds between camera checks
WAIT_TIME = 0.5

# Command strings dictating direction to move the camera.
COMMAND_UP = "U"
COMMAND_DOWN = "D"
COMMAND_LEFT = "L"
COMMAND_RIGHT = "R"
COMMAND_STAY = "X"

def calc_adjustment():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = face_classifier.detectMultiScale(
            gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40,40)
        )

    if (len(face) == 0):
        return (COMMAND_STAY, 0, 0)

    center_y, center_x = gray_image.shape
    center_x = center_x / 2
    center_y = center_y / 2
    face_x, face_y = center_x, center_y
    dx, dy = 9999, 9999


    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
        cur_face_x = x + w/2
        cur_face_y = y + h/2

        cur_dx = cur_face_x - center_x
        cur_dy = cur_face_y - center_y
        if (cur_dx + cur_dy < dx + dy):
            dx, dy = cur_dx, cur_dy
            face_x, face_y = cur_face_x, cur_face_y

    cv2.line(frame, (int(center_x), int(center_y)), (int(face_x), int(face_y)), (0, 0, 255), 4)

#    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#    plt.figure(figsize=(20,10))
#    plt.imshow(img_rgb)
#    plt.axis('off')
#    plt.show()


    if (abs(dx) > abs(dy)):
        if (dx > DEADZONE):
            return (COMMAND_LEFT if MIRROR else COMMAND_RIGHT,
                    CAMERA_SPEED, min(dx / CAMERA_SPEED, WAIT_TIME))
        elif (dx < -DEADZONE):
            return (COMMAND_RIGHT if MIRROR else COMMAND_LEFT,
                    CAMERA_SPEED, min(-dx / CAMERA_SPEED, WAIT_TIME))
    else:
        if (dy > DEADZONE):
            return (COMMAND_DOWN, CAMERA_SPEED, min(dy / CAMERA_SPEED, WAIT_TIME))
        elif (dy < -DEADZONE):
            return (COMMAND_UP, CAMERA_SPEED, min(-dy / CAMERA_SPEED, WAIT_TIME))

    # if we got here, we're in the deadzone
    return (COMMAND_STAY, 0, 0)

while (True):
    command = f"{COMMAND_STAY}0_0"
    try:
        direction, speed, time = calc_adjustment()
        command = f"{direction}{speed}_{time}"
    except:
        print("failed to get camera data")
    print(command)
    for outfilepath in OUTPUTS:
        try:
            with open(outfilepath, "a+") as outfile:
                outfile.write(command + "\n")
        except Exception as e:
            print("Failed to write to file", outfilepath)
            print(e)

    sleep(WAIT_TIME)
