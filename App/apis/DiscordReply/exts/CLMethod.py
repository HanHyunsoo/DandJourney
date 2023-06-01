# Channel Method

from . import BotSettings, PostAgent

"""
Channel Method Group:
채널 운영과 관련된 모든 콘텐츠를 여기에 배치합니다.
채널 전환, 채널 분리 및 기타 기능 포함
"""

# Switch Channel
def ChannelSwitch(ctx):
    if BotSettings["BotOpt"]["USE_CHANNEL"]:
        PostAgent.RefreshChannel(str(ctx.channel.id))

# Isolation Channel