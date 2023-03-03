from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
from ntcore import NetworkTableInstance, EventFlags
import time

ntinst = NetworkTableInstance.getDefault()
ntinst.startServer()
table = ntinst.getTable("Vision")

CameraServer.startAutomaticCapture()

while True:
    table.putNumber("MyNUMBER", 10)
    time.sleep(1)