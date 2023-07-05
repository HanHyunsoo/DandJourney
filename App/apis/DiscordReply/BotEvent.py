import os

from interactions import Extension, listen, Client

from interactions.api.events import MessageCreate, MessageUpdate

from . import BotSettings, PostAgent, SystemQueue, DQueueFQID

from .exts.CPMethod import CreateMultipleButtons

from .utils.MsgGene import CreateAgency, CreateMsg, QueueParse
from .utils.EmbGene import ImageEmb, DescribeEmb

from pymongo import MongoClient

'''
Event Listen Class
'''
class BotEventCls(Extension):
    def __init__(self, client: Client) -> None:
        self.client = client

        UVComponent = CreateMultipleButtons(ButtonName = ["U1", "U2", "U3", "U4", "V1", "V2", "V3", "V4", "🔁 Refresh", "🈴 Mix Them"], 
                                            custom_idDic = {"🔁 Refresh":"Refresh", "🈴 Mix Them":"BlendG"}, padding = [4,4,2], disableDic = {"🈴 Mix Them": True}, instantiation=True)
        # 주목, 세 번 더.U버튼에 실행 순서가 있습니다()메시지 업데이트 전송 중.on_MessageUpdate, 에 대하여on_MessageCreate도달불가
        # 현재 버튼이 거의 없다는 것을 감안할 때, 안정적일 때,UV대기열에 병합하여 공간 사용량 줄이기
        # 따라서 일부 버튼을 클릭할 수 없는 경우 먼저 언급할 필요가 없습니다.Issus
        MakeVComponent = CreateMultipleButtons(ButtonName = ["🔉 Describe", "🎁 Make Variations", "🔄 Remaster", "💡 Add Prompt", "🌈 Light Refinement", "🌈 Detail Refinement", "🌈 Reality Refinement"], 
                                            custom_idDic = {"🔉 Describe": "DescribeU", "🎁 Make Variations": "VariationU", "🔄 Remaster": "Remaster", "💡 Add Prompt": "RePrompt", 
                                                            "🌈 Light Refinement": "LightU", "🌈 Detail Refinement": "DetailU", "🌈 Reality Refinement": "RealityU"}, 
                                            disableDic={"🔉 Describe": True, "💡 Add Prompt": True}, padding = [2,2,3], instantiation = True)
        
        self.UVComponent = UVComponent[1] if UVComponent[0] else None
        self.MakeVComponent = MakeVComponent[1] if MakeVComponent[0] else None
        self.describeBox = []
        print("버튼 인스턴트화 완료")

        db_url = os.environ.get('MONGODB_URI')
        db_username = os.environ.get('MONGODB_USERNAME')
        db_password = os.environ.get('MONGODB_PASSWORD')
        db_name = os.environ.get('MONGODB_DBNAME')

        self.mongo_client = MongoClient(
            db_url,
            username=db_username,
            password=db_password
        )

        self.db = self.mongo_client[db_name]


    @listen()
    async def on_ready(self):
        print("Bot Ready!")
        print(SystemQueue.queueAllItem(length=True))

    @listen()
    async def on_MessageUpdate(self, event: MessageUpdate, **kwargs):

        message = event.after
        if message.author.bot:
            try:
                if message.author.username == "Midjourney Bot" and message.interaction.name == "describe":
                    if message.id not in self.describeBox:

                        self.describeBox.append(message.id)
                        # 임시 글쓰기 전용.Discord위
                        # Describe문제는 훌륭합니다. 사진이 통과되면 대기열을 막기 쉽습니다. 시간에 따라 대기열 요소를 지우기 전에 사용하는 것이 좋습니다.
                        # API사용 이러한 종류의 쓰기를 사용하지 마십시오. 대기열 효과를 차단합니다.User바인딩
                        # 기능을 구현하기 위해 구성 요소 버튼을 추가하는 것은 권장되지 않습니다. 때로는 블랙리스트에 있는 단어를 생성하여 프로세스를 차단합니다.
                        _DiscordQueue = SystemQueue.find_queue(DQueueFQID)[1].find("Mode", "DC")[0]
                        _emb = DescribeEmb(message.embeds[0].description, _DiscordQueue["Image"])

                        signalChannel = self.client.get_channel(int(_DiscordQueue["Channel"] if BotSettings["BotOpt"]["AGENT_SIGN"] else message.channel.id))
                        await signalChannel.send(content = "<@{}>".format(_DiscordQueue["User"]), embeds = _emb, attachments=[])

                        remove_number = lambda x: x[4:]
                        original_descriptions = _emb.description.split('\n\n')
                        filtered_descriptions = list(map(remove_number, original_descriptions))

                        print(filtered_descriptions)

                        self.db['images'].insert_one(
                            {
                                "url": _emb.image.url,
                                "descriptions": filtered_descriptions
                            }
                        )

                        SystemQueue.delete_queue_value(DQueueFQID, _DiscordQueue["JobID"])
                        print(SystemQueue.queueAllItem(length=True))

                    else:
                        self.describeBox.remove(message.id)
            except AttributeError as e:
                pass




    @listen()
    async def on_MessageCreate(self, event: MessageCreate, **kwargs):
        message = event.message
        if message.content == "": return
        if message.author.bot:
            try:
            # 판단 조건의 수 감소，기타 방치된 병합
            # 테스트한 항목은 삭제할 수 없습니다MidJourney원본 메시지，그렇지 않으면, 예.404_No_Message，중복 생성에 짜증이 난다면，생성된 콘텐츠를 저장하기 위해 섹션을 열 수 있습니다.

            # 前置 取出队列의数据
                Queue_msg = QueueParse(message.content, SystemQueue)

            # 1：메시지가Midjourney보내기，관련 정보에 접근할 수 있습니다.，이 메시지에 자동으로 회신하세요.targetID 와 targetHash

            # update 1:여기 있습니다.bug그러나 일시적으로 메시지를 통해 대기열의 버튼에 의해 트리거되는 대기열 정보를 가져올 수 없습니다(JobID버튼으로 통과할 수 없음)
            #          이 함수는 이제 시간차 방식으로 구현됩니다.Midjourney의 답장이 시간 순서대로 트리거되지 않으면 메시지 전달 객체가 비정상 상태가 됩니다.bug
            #          update 1 for Discord: 현재 두 개의 대기열이 사용되며, 각 녹음은 생성에 시간이 걸립니다.(예를 들어,Imagine/Blend지시 대기 중)시간이 필요하지 않은 작업 및 작업(U세분화/Describe)
            #          update 1 for Api:다음 메시지를 받은 후 마지막 반복 메시지를 삭제하거나 요청을 보낸 후 일시 중지합니다.user메시지 수신

                if message.attachments and Queue_msg[0] and message.author.username == "Midjourney Bot":

                    msgID = Queue_msg[1][1].queue_name
                    Qmsg = Queue_msg[1][1].find("JobID",Queue_msg[1][0])
                    if not Qmsg:
                        Qmsg = Queue_msg[1][1].find("JobID",Queue_msg[1][0], dim = -2)
                    agency = CreateAgency(message, Qmsg[0], msgID)
                    await message.reply(content = agency)

            # 2：메시지가Bot보내기，이미지 작업에 대한 내용입니다.，그 다음에 객체를 가져오고, 이 시점에서 그림을 가리키고,UV세분화
                if message.author.username == BotSettings["BotInfo"]["Name"] and "Get Bot Message for" in message.content:
                    _mode, _user, _embed, _channel, _JobID, _msgJobID = ImageEmb(message)
                    signalChannel = self.client.get_channel(int(_channel if BotSettings["BotOpt"]["AGENT_SIGN"] else message.channel.id))
                    if _mode == "UV" or ("BT" in _mode and 4 <= int(_mode[2:]) < 14):
                        await signalChannel.send(content = _user, components = self.UVComponent, embeds = _embed, attachments=[])
                    elif _mode == "MV" or ("BT" in _mode and int(_mode[2:]) < 4):
                        await signalChannel.send(content = _user, components = self.MakeVComponent, embeds = _embed, attachments=[])
                    else:
                        pass
                    SystemQueue.delete_queue_value(_msgJobID, _JobID)
                    await message.delete(delay=5)
                    print(SystemQueue.queueAllItem(length=True))


            except IndexError as e:
                pass

        return


def setup(bot):
    print("Init BotEvent.py")
    BotEventCls(bot)