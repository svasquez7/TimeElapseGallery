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

DEVICEID = "My-RaspberryPi-3b"
PROJECTNAME = "IOT Fun"
HUB_CONNECTION_STRING = "HostName=TimeElapseFun.azure-devices.net;DeviceId=GitHubUser;SharedAccessKey=Y8TPJJKHobcN0ciOdmzxM5HbE+BxKUcyTIcywv0JCVw="
BLOB_PROTOCOL = IoTHubTransportProvider.HTTP

MESSAGE_PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
ISSENDING = False

PATHTOFILE = '/home/pi/Pictures/'
FILENAME = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
MSG_TXT = "{\"deviceID\": \"%s\", \"projectName\": \"%s\",\"frameName\": \"%s\"}"

def blob_upload_conf_callback(result, user_context):
    if str(result) == 'OK':
        print ( "...file uploaded successfully." )
    else:
        print ( "...file upload callback returned: " + str(result) )
		
def take_picture():
    try:
        print ( "Taking picture, FILENAME: " + FILENAME )
        camera.start_preview()
        sleep(7)
        camera.capture(PATHTOFILE + FILENAME)
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

def iothub_file_upload():    
    client = iothub_client_init(BLOB_PROTOCOL)
    f = open(PATHTOFILE + FILENAME, "rb")
    content = base64.b64encode(f.read())
    client.upload_blob_async(FILENAME, content, len(content), blob_upload_conf_callback, 0)
    sleep(7)
    

def iothub_client_post_message():
    global ISSENDING
    ISSENDING = True
    while ISSENDING:
        message_client = iothub_client_init(MESSAGE_PROTOCOL)    
        msg_txt_formatted = MSG_TXT % (DEVICEID, PROJECTNAME, FILENAME)
        message = IoTHubMessage(msg_txt_formatted)
        # Send the message.
        print( "Sending message: %s" % message.get_string() )
        message_client.send_event_async(message, send_confirmation_callback, None)
        time.sleep(7)



if __name__ == '__main__':
    print ( "Starting process of taking pic and uploading to IOT HUB" )
    print ( "    BLOB_PROTOCOL %s" % BLOB_PROTOCOL )
    print ( "    Connection string=%s" % HUB_CONNECTION_STRING )
    
    take_picture()     
    iothub_file_upload()   
    iothub_client_post_message()
	