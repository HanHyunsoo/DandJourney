from .. import BotSettings
from .. import Banned_Word, DjPromptDic

from .JobDispatch import Dispatcher

DQueueID = "55100"
DQueueFQID = "55110"
SystemQueue = Dispatcher.Job()

SystemQueue.create_queue(DQueueID, 100, "Discord", is_isolation = True)
DiscordQueue = SystemQueue.find_queue(DQueueID)

SystemQueue.create_queue(DQueueFQID, 100, "DiscordQuick", is_isolation = True)
DiscordQueue = SystemQueue.find_queue(DQueueFQID)

print("데이터 시스템 큐 초기화됨, 현재 큐:{}".format(SystemQueue.queueList()))