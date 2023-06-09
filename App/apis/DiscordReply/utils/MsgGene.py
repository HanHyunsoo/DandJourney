import re, requests

from . import DQueueFQID

def CreateMsg(message):
    # 文本모드  已弃用
    user, result = message.content.split("|")[-2:]
    msg = re.sub(r"<.*?>|\*", "", message.get_referenced_message().content)
    targetID = str(message.message_reference.message_id)
    targetHash = str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0])
    return "**{}제어판**\n키워드：{}\nID：{}\nHash：{}\n그림 생성：{}".format(user, msg, targetID, targetHash, result), result


def CreateAgency(message, _Queue, msgID):
    imgURL = message.attachments[0].url
    _Mode = 'MV' if _Queue["Mode"] == "UV" and "- Image #" in message.content else _Queue["Mode"]
    
    return "Get Bot Message for |{M}|<@{U}>|{I} |{C}|{J}|{MJ}".format(M = _Mode, U = _Queue["User"], I = imgURL, 
                                                                C = _Queue["Channel"], J = _Queue["JobID"], 
                                                                MJ = msgID)


def QueueParse(content, JobManager):
    try:
        if "<#" in content:
            Job_id = re.findall(r"<#(.*?)>", content)[0]
        elif "https://s.mj.run/" in content:
            print("Loading URL ...")
            _url = re.findall("<(https?://.*?)>", content)[0]
            print("Get URL information!")
            Job_id = requests.get(_url).url.split("_")[-1].split(".")[0]
        else:
            return (False, "JobID not found in the content")
        # 임시적 글쓰기, 만약Upscaled메소드가 안정적이면Discord기본 대기열
        
        if "- Image #" in content or "- Upscaled" in content:
            JobQueue = JobManager.find_queue(DQueueFQID)
        else:
            JobQueue = JobManager.find_queue(Job_id[10:15])
        return (True, (Job_id, JobQueue[1])) if JobQueue[0] else (False, JobQueue[1])
    except IndexError:
        return (False, "JobID not found in the content")