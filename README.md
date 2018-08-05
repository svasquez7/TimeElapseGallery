# Time Elapse Gallery

The code in this repository can be used to create a gif by uploading a series of photos in jpg format.

The following file has successfully been ran on a Raspberry Pi 3B+, to run the code you must enter a unique devideid which is a string
and also a project name. The code is ment for time elapse photography, there is also a config for how many frames its going to take and how many
seconds between frames. File: Time_Elapse_Counter_V1-0.py
 
 Upon uploading the frame you can view the your project/gif here: http://timeelapsegallery.azurewebsites.net
 
 You can also change the frame rate for your project/gif by a post at the following api, the api will re-splice your photos into a gif with the milisecond frame rate posted. Fill in your project name and deviceid for best results.
 
 Action: Post
 
 Endpoint: http://timeelapsegallery.azurewebsites.net/api/frame/[projectname]
 
 payload:
 
 {
	"deviceID": "",
	"projectName": "",
	"FrameRateMiliseconds": 10
}
