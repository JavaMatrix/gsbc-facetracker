# GSBC Face Tracker
A utility for tracking a face on a webcam using OpenCL on a Raspberry Pi. This is designed to work with an external controller. It sends data in the format `Ax_y)` where `A` is the direction to move (`U` up, `D` down, `L` left, `R` right, `X` stay), `x` is the speed the camera should move in pixels/s, and `y` is the amount of time the camera should move at that speed in seconds.

# Configuration
Several configurable constants are declared at the top of tracker.py:
 - `CAMERA_SPEED`: The speed to give to the controller, in pixels/sec.
 - `DEADZONE`: The distance in pixels that the face must be from the center of the screen to trigger a camera movement.
 - `MIRROR`: True if the video feed is mirrored, false if it is not. This is probably TRUE on a webcam-type setup, and FALSE otherwise.
 - `OUTPUTS`: A list of files to which the program should write its output. These may be actual files or virtual devices, but for the latter, the program may need to be run in su.
 - `WAIT_TIME`: The amount of time to wait between checks. This is also the maximum movement time that the program will send to the controller.
 - `COMMAND_XYZ`: There is one constant defined for each direction the camera may move. Set these to whatever is expected by the controller for each direction.

# Note to Collaborator
If you are making the controller, the output can be changed as necessary. For example, if only integer speeds and times should be provided, or time should be sent in milliseconds instead of seconds, this is easily done.
