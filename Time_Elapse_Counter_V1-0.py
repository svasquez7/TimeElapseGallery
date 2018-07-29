import time
import sys
import iothub_client
import os
import base64
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

from picamera import PiCamera
from time import sleep
from datetime import datetime

camera = PiCamera()

camera.resolution = (2592, 1944)
camera.framerate = 15
#camera.rotation =90

NUMBER_OF_FRAMES = 60
SECONDS_BETWEEN_FRAMES = 120
#****************** Fill in a deviceid and projectname***********************
#********** deviceid can be any string to identify you, example: mikes pi 3b 1, mikes-raspberrypi-zerowifi *********************
#*********** project name should describe the pictures your gonna capture, example: Colorado Sunset, My garden.....********
DEVICEID = "git-hub-user"
PROJECTNAME = ""
#*******************************************************************************************************************************
HUB_CONNECTION_STRING = "HostName=TimeElapseFun.azure-devices.net;DeviceId=GitHubUser;SharedAccessKey=Y8TPJJKHobcN0ciOdmzxM5HbE+BxKUcyTIcywv0JCVw="
BLOB_PROTOCOL = IoTHubTransportProvider.HTTP

MESSAGE_PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
ISSENDING = False

PATHTOFILE = '/home/pi/Pictures/'
MSG_TXT = "{\"deviceID\": \"%s\", \"projectName\": \"%s\",\"frameName\": \"%s\"}"

def blob_upload_conf_callback(result, user_context):
    if str(result) == 'OK':
        print ( "...file uploaded successfully." )
    else:
        print ( "...file upload callback returned: " + str(result) )
		
def take_picture(file_name):
    try:
        print ( "Taking picture, FILENAME: " + file_name )
        camera.start_preview()
        sleep(7)
        camera.capture(PATHTOFILE + file_name)
        camera.stop_preview()	
    except:
        camera.stop_preview()
        print ("an error occured capturing picture.")

def send_confirmation_callback(message, result, user_context):
    global ISSENDING
    if str(result) == 'OK':
        ISSENDING = False
   
    print ( "IoT Hub responded to message with status: %s" % (result) )
    print ( "ISSENDING: %s" % (ISSENDING) )

def iothub_client_init(protocol):
    # Create an IoT Hub client
    client = IoTHubClient(HUB_CONNECTION_STRING, protocol)
    return client

def iothub_file_upload(file_name):    
    client = iothub_client_init(BLOB_PROTOCOL)
    f = open(PATHTOFILE + file_name, "rb")
    content = base64.b64encode(f.read())
    client.upload_blob_async(file_name, content, len(content), blob_upload_conf_callback, 0)
    

def iothub_client_post_message(file_name):
    global ISSENDING
    ISSENDING = True
    while ISSENDING:
        message_client = iothub_client_init(MESSAGE_PROTOCOL)    
        msg_txt_formatted = MSG_TXT % (DEVICEID, PROJECTNAME, file_name)
        message = IoTHubMessage(msg_txt_formatted)
        # Send the message.
        print( "Sending message: %s" % message.get_string() )
        message_client.send_event_async(message, send_confirmation_callback, None)
        time.sleep(7)



if __name__ == '__main__':
    print ( "Starting process of taking pic and uploading to IOT HUB" )
    print ( "    BLOB_PROTOCOL %s" % BLOB_PROTOCOL )
    print ( "    Connection string=%s" % HUB_CONNECTION_STRING )   

    frameCount = 0
    while frameCount <= NUMBER_OF_FRAMES:
        file_name = PROJECTNAME.replace(" ", "-") + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        take_picture(file_name)     
        iothub_file_upload(file_name)   
        iothub_client_post_message(file_name)

        if os.path.exists("demofile.txt"):
            os.remove(PATHTOFILE + file_name)

        frameCount = frameCount + 1
        time.sleep(SECONDS_BETWEEN_FRAMES)
	