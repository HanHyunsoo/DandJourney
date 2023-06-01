# Component Method
from . import interactions, Button, BotSettings

"""
Component Method Group:
모든 구성 요소 관련 콘텐츠를 여기에 배치하십시오
구성 요소 빌드 포함，귀속부품 경청，구성 요소 제거와 같은 기능
"""

# Component Handle
def ActivateButtons(components: list, padding: list) -> tuple:
    """
    Registration：Turns the list of components into an object\\
    components：    귀속부품 목록\\
    padding：       구성 요소 배열
    """
    __tempComList, __tempChecker = [], 0
    if not padding: padding = [5]*5

    if max(padding) > 5: return (False, "The number of components in a single column exceeds the allowed value. Initialization failed")
    
    for __row in padding:
        if __row < len(components[__tempChecker:]):
            __tempComList.append(interactions.ActionRow(*components[__tempChecker : __tempChecker + __row]))
            __tempChecker += __row
        else:
            __tempComList.append(interactions.ActionRow(*components[__tempChecker :]))
            break
    return (True, __tempComList)


# Component Create
def CreateMultipleButtons(ButtonName: list,  styleDic: dict = None, custom_idDic: dict = None, emojiDic: dict = None, padding: list = None, disableDic: dict = None, instantiation: bool = False) -> list or object:
    """
    Component：Generate multiple button\\
    ButtonName：    버튼 구성 요소 이름 목록\\
    custom_id：     버튼 식별자, 지정되지 않은 경우,ButtonName매치 Usage : {ButtonName : ButtonID}\\
    style:          버튼 스타일 Usage : {ButtonName : ButtonStyle} \\
    emoji：         이모티콘 사용 여부 Usage : {ButtonName : ButtonEmoji}\\
    disable：       비활성화할 버튼 목록 Usage : {ButtonName : Disabled}\\
    
    padding：       구성 요소 배열\\
    instantiation： 인스턴스화 버튼 목록이 필요한 경우 예 설정
    """
    __components = []
    if len(ButtonName) >= 25: return (False, "Description The number of messages reached the upper limit. Initialization failed")

    for _name in ButtonName:
        __components = CreateSingleButton(
                                                ButtonName = _name, 
                                                style = 2 if styleDic is None or _name not in styleDic else styleDic[_name],
                                                custom_id = _name if custom_idDic is None or _name not in custom_idDic else custom_idDic[_name],
                                                emoji = None if emojiDic is None or _name not in emojiDic else emojiDic[_name],
                                                disable = None if disableDic is None or _name not in disableDic else disableDic[_name],
                                                components = __components
                                            )
    return ActivateButtons(__components, padding) if instantiation else (True, __components)

def CreateSingleButton(ButtonName: str, style: int = 2, custom_id: str = None, emoji: str = None, disable: bool = False, components: list = [], index: int = None, instantiation: bool = False) -> list:
    """
    Component：Generate single button\\
    ButtonName:    버튼 이름\\
    style:         버튼 스타일\\
    custom_id：    버튼 식별자, 지정되지 않은 경우,ButtonName매치\\
    emoji：        이모티콘 사용 여부\\
    disable：      버튼을 비활성화 하시겠습니까?\\
    
    components：   추가할 새 버튼 목록\\
    index：        새 버튼 삽입 위치\\
    instantiation：인스턴스화 버튼 목록이 필요합니까?
    """
    components.insert(len(components) if index is None else index, Button(style = style, custom_id = custom_id if custom_id else ButtonName, label = ButtonName, emoji = emoji, disabled = disable))
    return ActivateButtons(components) if instantiation else components

# Component Delete


# Component Check
def ButtonClick(ctx: interactions.ComponentContext, styleNeed: int = 1, disable: bool = True, Switch: list = []) -> list:
    """
    Component：Click Button Method\\
    ctx 버튼 이벤트CommandContext
    styleNeed 버튼 스타일 지정，기본값으로 사용
    disable 버튼이 지정되어 있는지 여부，기본값으로 사용 안 함
    Switch 토글 목록，버튼 모드 변경 기본값
    """
    __tempList = []
    __buttonList = [interactions.ButtonStyle.PRIMARY, interactions.ButtonStyle.SECONDARY, interactions.ButtonStyle.SUCCESS, interactions.ButtonStyle.DANGER]
    for __action in ctx.message.components:
        __SecList = []
        for __component in __action.components:
            button = Button(style = __component.style, custom_id = __component.custom_id, label = __component.label, disabled = __component.disabled)
            if Switch:
                # 버튼 상태 토글
                if __component.custom_id == BotSettings[Switch[0]][Switch[1]] or __component.custom_id == ctx.component.custom_id:
                    button.style = __buttonList[1] if str(__component.style)=="1" else __buttonList[0] 
                    button.disabled = False if __component.disabled else True
            else:
                # 버튼 상태 설정
                if __component.custom_id == ctx.component.custom_id:
                    button.style = __buttonList[styleNeed-1]
                    button.disabled = disable
                else: pass
            __SecList.append(button)
        __tempList.append(__SecList)
    return __tempList