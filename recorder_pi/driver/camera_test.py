import os
import sys
import configparser
import time
from datetime import datetime
import time
# from picamera2 import Picamera2
# from picamera2.encoders import H264Encoder

class CommandInstance():
    def __init__(self,type,payload):
        self.type = type
        self.payload = payload
    def __str__(self):
        print(self,self.type)

def readConfig(file):
    read_ini = configparser.ConfigParser()
    read_ini.read(file)
    cam_value = read_ini.items('Camera')
    path_value = read_ini.items('Path')
    other_value = read_ini.items('Other')
    camera_config = {}
    path_config = {}
    other_config = {}
    for i in cam_value:
        camera_config[i[0]] = i[1]
    for i in path_value:
        path_config[i[0]] = i[1]
    for i in other_value:
        other_config[i[0]] = i[1]
    #print(camera_config,other_config,path_config)
    return (camera_config,path_config,other_config)

def generateCommand_str(config_dict):
    event_height     = config_dict["height"]
    event_width      = config_dict["width"]
    event_duration   = config_dict["duration"]
    event_focus      = config_dict["lens-position"]

    event_height     = event_height   if type(event_height) == str    else str(event_height)
    event_width      = event_width    if type(event_width) == str     else str(event_width)
    event_duration   = event_duration if type(event_duration) == str  else str(event_duration)
    event_focus      = event_focus    if type(event_focus) != str     else event_focus

    cmd_list = ["libcamera-vid", "--save-pts timestamps.txt"]
    if "type" in config_dict.keys():
        cmd_list[0] = cmd_list[0] if config_dict["type"] == "libcamera-vid" else "libcamera-still"
        cmd_list[1] = "" if config_dict["type"] == "libcamera-vid" else "libcamera-still"
    else:
        pass
    # camera_config,path_config,other_config = config_dict
    cmd_list.append("--height")
    cmd_list.append(event_height)
    cmd_list.append("--width")
    cmd_list.append(event_width)
    if cmd_list[0] == "libcamera-vid":
        cmd_list.append("--framerate")
        cmd_list.append(
            config_dict["framerate"] if type(config_dict["framerate"]) == str else str(config_dict["framerate"]))
    else:
        pass
    cmd_list.append("-t")
    cmd_list.append(event_duration)
    if (config_dict["focus"] == "continue"):
        pass
        # cmd_list.append("--continue-autofocus")
    if (config_dict["preview"] == "qt-preview"):
        cmd_list.append("--qt-preview")
    root_path_str = config_dict["root_path"]
    video_path_str = config_dict["raw_path"]
    filename_str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    cmd_list.append("-o")
    if cmd_list[0] == "libcamera-vid":
        cmd_list.append(root_path_str + "/" + video_path_str + "/" + filename_str + ".h264")
    else:
        cmd_list.append(root_path_str + "/" + video_path_str + "/" + filename_str + ".jpg")

    if event_focus is None:
        cmd_list.append("--autofocus-mode=auto")
    else:
        event_focus = event_focus if type(event_focus) == str else str(event_focus)
        cmd_list.append("--autofocus-mode=manual")
        cmd_list.append("--lens-position="+event_focus)

    cmd_str = " ".join(cmd_list)
    return CommandInstance(payload=cmd_str,type="bash_cmd")



def CaptureVideo(commandInstance) -> (str,str) or None:
    """
    Introduction: Capture the video by executing bash command and return the file path.

    :param commandInstance: Class commandinstance
    :return: string tuple, first is the current filename and the second is the path
    """

    if commandInstance.type == "bash_cmd":
        os.system(commandInstance.payload)
        return
    return


def cameraDist2lensDist(camDist:float) -> float:
    lensDist = camDist / 100
    lensDist = 1 / lensDist if lensDist != 0 else 100000
    return lensDist



if __name__ == "__main__":
    a = readConfig("/home/pi/camera_app/config.ini")
    a1 = generateCommand_str(a)
    CaptureVideo(a1)
    #generateCommand_api()
