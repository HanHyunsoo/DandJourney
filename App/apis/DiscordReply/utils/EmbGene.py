from . import interactions, BotSettings

import re

def AboutEmb():
    embed = interactions.Embed(title = "*****DandJourney*****", description = '연애 메시지를 담은 로봇 포워딩', color=0x00ff00, url='https://github.com/yuexdang/DandJourney',
                               images=[interactions.EmbedAttachment(url="https://opengraph.githubassets.com/70433925c505ce837dda9bab06af0101f3ac5b592acc6763a52b04b9ef059142/yuexdang/DandJourney")])
    embed.set_image('https://opengraph.githubassets.com/70433925c505ce837dda9bab06af0101f3ac5b592acc6763a52b04b9ef059142/yuexdang/DandJourney')
    embed.add_field(name = '——'*15, value = " ", inline = False)
    embed.add_field(name = '현재 로봇 이름', value = BotSettings["BotInfo"]["Name"], inline = True)
    embed.add_field(name = '현재 버전', value = BotSettings["BotInfo"]["version"], inline = True)
    embed.set_footer(text = 'Made By Yuexdang Universe D Team', icon_url = 'https://user-images.githubusercontent.com/56034408/234861839-7cddd103-e597-4029-b514-063c4bca5227.png')
    return embed

def HelpEmb():
    embed = interactions.Embed(title = "*****DandJourney*****", description = '연애 메시지를 담은 로봇 포워딩', color=0x00ff00)
    embed.add_field(name = '——'*6, value = " ", inline = False)
    embed.add_field(name = 'DandJourney 명령어 집합', value = " ", inline = True)
    embed.add_field(name = '/dj `prompt` `*args`', value = "그림 생성，첨부 버전에서 지원되는 모든 매개 변수", inline = False)
    embed.add_field(name = '/ddescribe `image`', value = "설명 이미지", inline = False)
    embed.add_field(name = '/dblend `image(s)` `dim`', value = "믹스 픽쳐스，최대 지원5장현수", inline = False)
    embed.add_field(name = '/dsettings', value = "제어판 열기", inline = False)
    embed.add_field(name = '/aboutdj', value = "소개DandJourney", inline = False)
    embed.add_field(name = '/dhelp', value = "DandJourney사용 방법", inline = False)
    embed.set_footer(text = '자세한 내용은 다음을 참조하십시오.Usage.md문서')
    return embed

def ImageEmb(message):
    mode, user, result, channel, jobID, msgJobID = message.content.split("|")[-6:]
    msg = re.sub(r'<(?!https?:\/\/\S+).*?>|\*', '', message.get_referenced_message().content)
    targetID = str(message.message_reference.message_id)
    targetHash = str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0])

    embed = interactions.Embed(title = "***DandJourney이미지 게시판***", description = ' ', color=0x3eede7)
    embed.add_field(name = '키워드:', value = msg, inline = False)
    embed.add_field(name = 'TargetID', value = targetID, inline = False)
    embed.add_field(name = 'TargetHash', value = targetHash, inline = False)
    embed.add_field(name = 'JobID', value = jobID if "BT" not in mode else jobID.split("#")[0], inline = False)
    embed.set_image(result)
    return mode, user, embed, channel, jobID, msgJobID

def DescribeEmb(description, image):
    embed = interactions.Embed(title = "***DandJourney설명 게시판***", description = description, color=0x3eede7)
    embed.set_image(image)
    return embed