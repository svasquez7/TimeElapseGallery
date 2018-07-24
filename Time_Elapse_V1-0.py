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

DEVICEID = "SVasquez-RaspberryPi3"
PROJECTNAME = "Local Yocal 1"
HUB_CONNECTION_STRING = "HostName=TimeElapseFun.azure-devices.net;DeviceId=SVasquez-RaspberryPi3;SharedAccessKey=LfgWJvx/RKd8MyebWRyQA6xOUiNGGrfmFDBjcZzFBJ4="
BLOB_PROTOCOL = IoTHubTransportProvider.HTTP

MESSAGE_PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

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
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_file_upload():    
    client = IoTHubClient(HUB_CONNECTION_STRING, BLOB_PROTOCOL)
    f = open(PATHTOFILE + FILENAME, "rb")
    content = base64.b64encode(f.read())
    client.upload_blob_async(FILENAME, content, len(content), blob_upload_conf_callback, 0)
    sleep(7)
    

def iothub_client_post_message():

    message_client = IoTHubClient(HUB_CONNECTION_STRING, MESSAGE_PROTOCOL)    
    msg_txt_formatted = MSG_TXT % (DEVICEID, PROJECTNAME, FILENAME)
    message = IoTHubMessage(msg_txt_formatted)
    # Send the message.
    print( "Sending message: %s" % message.get_string() )
    message_client.send_event_async(message, send_confirmation_callback, None)


if __name__ == '__main__':
    print ( "Starting process of taking pic and uploading to IOT HUB" )
    print ( "    BLOB_PROTOCOL %s" % BLOB_PROTOCOL )
    print ( "    Connection string=%s" % HUB_CONNECTION_STRING )
    
    take_picture()     
    iothub_file_upload()   
    iothub_client_post_message()
	