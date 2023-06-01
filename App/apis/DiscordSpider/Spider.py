import requests

from .utils.payload import JsonImagine, JsonFast, JsonRelax, JsonBlend, JsonMorph, JsonRegImg, JsonDescribe

from . import BotSettings


class PostMethod():
    """
    상위 카테고리 PostMethod：
    이 메소드는 몇 가지 기본 매개 변수와 기본 메소드를 생성하고 구성하는 데 사용됩니다.
    이 클래스는 일부 동적 메소드를 추가하도록 사용자 정의할 수 있습니다
    """
    def __init__(self, MID_JOURNEY_ID : str, SERVER_ID : str, CHANNEL_ID : str, VIP_TOKEN : str) -> None:
        self.MID_JOURNEY_ID = MID_JOURNEY_ID
        self.SERVER_ID = SERVER_ID
        self.CHANNEL_ID = CHANNEL_ID
        
        self.header = {'authorization' : VIP_TOKEN}
        self.URL = "https://discord.com/api/v9/interactions"

        self.StorageURL = "https://discord.com/api/v9/channels/" + CHANNEL_ID + "/attachments"

    def __ResponseCheck(self, Response):
        """
        요청 상태 확인，수업 중 방법
        """
        if Response.status_code >= 400:
            return (False, "ResponseError in Location:{}, Msg:{}, Code:{}".format("ResponseCheck" ,Response.text, Response.status_code))
        return (True, Response)

    def GetResponse(self, json : dict) -> bool:
        """
        요청 상태 확인，부류 외 방법
        """
        try:
            response = requests.post(url = self.URL, json = json, headers = self.header)
            return self.__ResponseCheck(response)
        except Exception as e:
            return (False, "ResponseError in Location:{}, Msg:{}".format("GetResponse", e))

    def ImageStorage(self, ImageName : str, ImageUrl : str, ImageSize : int, prompt: str) -> tuple:
        """
        유언Discord역전사슬의 재처리，내부 체인을 가져옵니다.
        update 1: 현재 필수 매개 변수 추가 지원JobID
        """
        try:
            ImageName = ImageName.split(".")
            ImageName = "{}_{}.{}".format(ImageName[0], prompt, ImageName[1])

            _response = requests.post(url = self.StorageURL, json = JsonRegImg(ImageName, ImageSize), headers = self.header)
            if self.__ResponseCheck(_response)[0]:
                __Res = _response.json()["attachments"][0]
                upload_url = __Res["upload_url"]
                upload_filename = __Res["upload_filename"]

                __response = requests.get(ImageUrl, headers={"authority":"cdn.discordapp.com"})
                if self.__ResponseCheck(__response)[0]:

                    ___response = requests.put(upload_url,data=__response.content, headers={"authority":"discord-attachments-uploads-prd.storage.googleapis.com"})
                    if self.__ResponseCheck(___response)[0]:
                        return (True, (ImageName, upload_filename))
                    else:
                        return (False, "StorageError in Location:ImageStorage, Msg:Can't Storage!")
                else:
                    return (False, "ReadError in Location:Image, Msg:Image is not exist!")
            else:
                return (False, "ResponseError in Location:GetResponse, Msg:Fail to get Response from Discord!")
        except Exception as e:
            return (False, "RunningError in Location:{}, Msg:{}".format("ImageStorage", e))

    def RefreshChannel(self, ChannelID : str) -> None:
        """
        채널 새로고침
        """
        self.CHANNEL_ID = ChannelID
        return


class DecoratorCls:
    """
    데코레이터 클래스：
    이 클래스에 필요한 모든 데코레이터를 저장합니다.
    예약된 위치，지금은 안돼요
    """
    def ChannelDC(self, func):
        def wrapper(innerSelf):
            pass
            func(innerSelf)
        return wrapper
    

class DiscordPost(PostMethod):
    DecoCls = DecoratorCls()
    def __init__(self) -> None:
        PostMethod.__init__(self, BotSettings["BotCode"]["MID_JOURNEY_ID"], BotSettings["BotCode"]["SERVER_ID"], BotSettings["BotCode"]["CHANNEL_ID"], BotSettings["BotCode"]["VIP_TOKEN"])
        pass

    def Imagine(self, prompt : str, channel : str = None) -> object:
        """
        이미지 생성용
        """
        __payload = JsonImagine(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID, 
                                prompt)
        response = self.GetResponse(json = __payload)
        return response

    def Upscale(self, index : int, messageId : str, messageHash : str, channel : str = None):
        """
        이미지 확대에 사용 U버튼
        """
        __payload = JsonMorph(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID,
                              index, messageId, messageHash, "upsample")
        response = self.GetResponse(json = __payload)
        return response
    
    def Variation(self, index : int, messageId : str, messageHash : str, solo : bool = False, channel : str = None):
        """
        이미지 분할에 사용됨 V버튼
        """
        __payload = JsonMorph(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID,
                              index, messageId, messageHash, "variation", solo=solo)
        response = self.GetResponse(json = __payload)
        return response
    
    def Remaster(self, index : int, messageId : str, messageHash : str, channel : str = None):
        """
        큰 이미지 세분화용 Remaster버튼
        """
        __payload = JsonMorph(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID,
                              index, messageId, messageHash, "remaster", solo = True)
        response = self.GetResponse(json = __payload)
        return response

    def LUpscale(self, index : int, messageId : str, messageHash : str, channel : str = None):
        """
        큰 이미지 빛 및 그림자 분할에 사용 Light Upscale Redo 버튼
        """
        __payload = JsonMorph(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID,
                              index, messageId, messageHash, "upsample_light", solo = True)
        response = self.GetResponse(json = __payload)
        return response

    def DUpscale(self, index : int, messageId : str, messageHash : str, channel : str = None):
        """
        큰 세부 세분화용 Detailed Upscale Redo 버튼
        """
        __payload = JsonMorph(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID,
                              index, messageId, messageHash, "upsample", solo = True)
        response = self.GetResponse(json = __payload)
        return response
    
    def BUpscale(self, index : int, messageId : str, messageHash : str, channel : str = None):
        """
        큰 이미지의 2차 분할에 사용됨 Beta Upscale Redo 버튼
        """
        __payload = JsonMorph(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID,
                              index, messageId, messageHash, "upsample_beta", solo = True)
        response = self.GetResponse(json = __payload)
        return response

    def Fast(self):
        """
        다이어그램 모드를 다음으로 전환::Fast
        """
        __payload = JsonFast(self.MID_JOURNEY_ID, self.SERVER_ID, self.CHANNEL_ID)
        response = self.GetResponse(json = __payload)
        return response
    
    def Relax(self):
        """
        다이어그램 모드를 다음으로 전환::Relax
        """
        __payload = JsonRelax(self.MID_JOURNEY_ID, self.SERVER_ID, self.CHANNEL_ID)
        response = self.GetResponse(json = __payload)
        return response

    def Blend(self, ImageSet : list, Dimensions : str, prompt : str, channel : str = None):
        """
        그림 블렌드
        """
        __options , __attachments = [], []
        for Image in ImageSet:
            if Image:
                response = self.ImageStorage(ImageName = Image.__getattribute__("filename"), ImageUrl = Image.__getattribute__("url"), ImageSize = Image.__getattribute__("size"), prompt = prompt)
                if response[0]:
                    __options.append({"type":11,"name":"image{}".format(len(__options)+1),"value":len(__options)})
                    __attachments.append({"id":str(len(__options)-1),"filename":response[1][0],"uploaded_filename":response[1][1]})

        if Dimensions != "--ar 1:1":
            __options.insert(2,{"type":3,"name":"dimensions","value":Dimensions})

        __payload = JsonBlend(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID, 
                              __options, __attachments)
        response = self.GetResponse(json = __payload)
        return response
    
    def Refresh(self, index : int, messageId : str, messageHash : str, channel : str = None):
        """
        사진을 새로고침하는 데 사용됩니다.
        """
        __payload = JsonMorph(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID,
                              index, messageId, messageHash, "reroll", solo=True)
        response = self.GetResponse(json = __payload)
        return response
    
    def Describe(self, Image : object, prompt : str, channel : str = None):
        """
        그림 설명에 사용됨
        """
        response = self.ImageStorage(ImageName = Image.__getattribute__("filename"), ImageUrl = Image.__getattribute__("url"), ImageSize = Image.__getattribute__("size"), prompt = prompt)
        if response[0]:
            __attachments = [{"id":0, "filename":response[1][0],"uploaded_filename":response[1][1]}]

        __payload = JsonDescribe(self.MID_JOURNEY_ID, self.SERVER_ID, channel if channel else self.CHANNEL_ID,
                                  __attachments)
        response = self.GetResponse(json = __payload)
        return response
    
    def RegisterImage(self, filename : str, filesize : int, url : str):
        """
        이미지 등록，추천 이미지 업로드
        """
        __payload = JsonRegImg(filename, filesize, url)
        response = self.GetResponse(json = __payload)
        return response
