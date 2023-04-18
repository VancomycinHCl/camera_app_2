import re

# 定义抽象工厂接口
class CameraFactory:
    def create_still(self):
        pass

    def create_vid(self):
        pass

# 定义具体的libcamera-still类
class LibCameraStill:
    def __init__(self,
                 H264_Folder:str="",
                 width:int=1920,
                 height:int=1080):
        self.type = "libcamera-still"
        self.H264_Folder= H264_Folder
        self.width= width
        self.height= height
        self._duration = 1000

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, duration_new: int) -> None:
        self._duration = duration_new

    @property
    def RefDict(self) -> dict:
        retDict = {
            "H264_Folder": self.H264_Folder,
            "width": self.width,
            "height": self.height,
            "duration": self._duration,
            "type" : self.type
        }
        return retDict
    @RefDict.setter
    def RefDict(self, dictIn: dict) -> None:
        dictIn_keys = dictIn.keys()
        if "H264_Folder" in dictIn_keys:
            self.H264_Folder = dictIn["H264_Folder"]
        if "width" in dictIn_keys:
            self.width = dictIn["width"]
        if "height" in dictIn_keys:
            self.height = dictIn["height"]
        if "duration" in dictIn_keys:
            self.duration = dictIn["duration"]
        if "type" in dictIn_keys:
            self.type = dictIn["type"]

    def setRefDict(self,refStr:str) -> None:
        # "libcamera-still -t 100000  --height 1080 asdfa -o hh.jpg"
        # 按照固定顺序 匹配 延时时间 宽度 高度 输出文件目录
        pattern = r"(?=(.*?-t\s+(\d+)))?(?=(.*?--width\s+(\d+)))?(?=(.*?--height\s+(\d+)))?(?=(.*?-o\s+(\S+)))?"
        # 进行匹配
        match = re.match(pattern, refStr)
        if match:
            self._duration = int(match.group(2)) if match.group(2) != None else self._duration
            self.width    = int(match.group(4)) if match.group(4) != None else self.width
            self.height   = int(match.group(6)) if match.group(6) != None else self.height
            self.H264_Folder = match.group(8)   if match.group(8) != None else self.H264_Folder
            # print(match.group(2))
            # print(match.group(4))
            # print(match.group(6))
            # print(match.group(8))
        else:
            pass


    @property
    def getType(self) -> str:
        return self.type

    def __str__(self):
        if type(self._duration) == int:
            self._duration = str(self._duration)
        if type(self.height) == int:
            self.height = str(self.height)
        if type(self.width) == int:
            self._duration = str(self.width)
        buffer = [self.type,"-t",str(self._duration),
                  "-o",self.H264_Folder,
                  "--width",str(self.width),"--height",str(self.height)]
        buffer = " ".join(buffer)
        return buffer


# 定义具体的libcamera-vid类
class LibCameraVid:
    def __init__(self, H264_Folder: str = "",
                 width: int = 1920,
                 height: int = 1080,
                 duration: int = 1000,
                 framerate: int = 25):
        self.type = "libcamera-vid"
        self.H264_Folder = H264_Folder
        self.width = width
        self.height = height
        self._duration = str(duration)
        self.framerate = str(framerate)

    @property
    def duration(self) -> int:
        return self._duration
    @duration.setter
    def duration(self, duration_new:int) -> None:
        self._duration = duration_new

    @property
    def RefDict(self) -> dict:
        retDict = {
            "H264_Folder": self.H264_Folder,
            "width": self.width,
            "height": self.height,
            "duration": self._duration,
            "framerate" : self.framerate,
            "type": self.type
        }
        return retDict
    @RefDict.setter
    def RefDict(self, dictIn: dict) -> None:
        dictIn_keys = dictIn.keys()
        if "H264_Folder" in dictIn_keys:
            self.H264_Folder = dictIn["H264_Folder"]
        if "width" in dictIn_keys:
            self.width = dictIn["width"]
        if "height" in dictIn_keys:
            self.height = dictIn["height"]
        if "duration" in dictIn_keys:
            self.duration = dictIn["duration"]
        if "framerate" in dictIn_keys:
            self.framerate = dictIn["framerate"]
        if "type" in dictIn_keys:
            self.type = dictIn["type"]

    def setRefDict(self,refStr:str) -> None:
        # "libcamera-still -o dsaf.h264 -t 1000 --width 1920 --height 1080 --framerate 25"
        pattern = r"(?=(.*?-t\s+(\d+)))?(?=(.*?--width\s+(\d+)))?(?=(.*?--height\s+(\d+)))?(?=(.*?-o\s+(\S+)))?(?=(.*?--framerate\s+(\d+)))?"
        match = re.match(pattern, refStr)
        print(match)
        if match:
            self._duration = int(match.group(2)) if match.group(2) != None else self._duration
            self.width = int(match.group(4)) if match.group(4) != None else self.width
            self.height = int(match.group(6)) if match.group(6) != None else self.height
            self.H264_Folder = match.group(8) if match.group(8) != None else self.H264_Folder
            self.framerate = match.group(10)   if match.group(10) != None else self.framerate
        else:
            pass



    @property
    def getType(self) -> str:
        return self.type

    def __str__(self):
        if type(self._duration) == int:
            self._duration = str(self._duration)
        if type(self.height) == int:
            self.height = str(self.height)
        if type(self.width) == int:
            self._duration = str(self.width)
        if type(self.framerate) == int:
            self.framerate = str(self.framerate)
        buffer = [self.type, "-t", str(self._duration),
                  "-o", self.H264_Folder,
                  "--width", str(self.width), "--height", str(self.height),
                  "--framerate",self.framerate]
        buffer = " ".join(buffer)
        return buffer

# 实现抽象工厂接口，用于创建具体的libcamera-still和libcamera-vid对象
class CameraFactoryImpl(CameraFactory):
    def create_still(self) -> LibCameraStill:
        return LibCameraStill()

    def create_vid(self) -> LibCameraVid:
        return LibCameraVid()


if __name__ == "__main__":
    # 使用抽象工厂模式创建对象
    factory = CameraFactoryImpl()
    b = factory.create_vid()
    print(b.getType)
    print(b.RefDict)
    b.setRefDict("libcamera-vid -t 100000 --width 1920  --height 1080  -o hh.jpg")
    print(b.RefDict)
    print(str(b))
    # my_object = MyClass(factory)