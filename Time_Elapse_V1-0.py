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

DEVICEID = ""
PROJECTNAME = ""
HUB_CONNECTION_STRING = "HostName=TimeElapseFun.azure-devices.net;DeviceId=" + DEVICEID +";SharedAccessKey=LfgWJvx/RKd8MyebWRyQA6xOUiNGGrfmFDBjcZzFBJ4="
BLOB_PROTOCOL = IoTHubTransportProvider.HTTP

MESSAGE_PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

PATHTOFILE = '/home/pi/Desktop/'
FILENAME = ""
MSG_TXT = "{\"deviceID\": %s, \"projectName\": %s,\"frameName\": %s}"

def blob_upload_conf_callback(result, user_context):
    if str(result) == 'OK':
        print ( "...file uploaded successfully." )
    else:
        print ( "...file upload callback returned: " + str(result) )
		
def take_picture():
	FILENAME = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
	camera.start_preview()
	sleep(7)
	camera.capture(PATHTOFILE + FILENAME)
	camera.stop_preview()	

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_file_upload():    
    client = IoTHubClient(HUB_CONNECTION_STRING, BLOB_PROTOCOL)
    f = open(PATHTOFILE + FILENAME, "rb")
    content = base64.b64encode(f.read())
    client.upload_blob_async(FILENAME, content, len(content), blob_upload_conf_callback, 0)
    iothub_client_post_message()

def iothub_client_post_message():

    client = IoTHubClient(HUB_CONNECTION_STRING, MESSAGE_PROTOCOL)
    print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
    
    msg_txt_formatted = MSG_TXT % (DEVICEID, PROJECTNAME, FILENAME)
    message = IoTHubMessage(msg_txt_formatted)

    # Send the message.
    print( "Sending message: %s" % message.get_string() )
    client.send_event_async(message, send_confirmation_callback, None)


if __name__ == '__main__':
    print ( "Simulating a file upload using the Azure IoT Hub Device SDK for Python" )
    print ( "    BLOB_PROTOCOL %s" % BLOB_PROTOCOL )
    print ( "    Connection string=%s" % HUB_CONNECTION_STRING )
    
    take_picture()
    iothub_file_upload()
	