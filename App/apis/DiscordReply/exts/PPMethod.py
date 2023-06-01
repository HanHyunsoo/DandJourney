# Prompt Method

from . import BotSettings
import re

"""
Prompt Method Group:
매개변수 작동과 관련된 모든 콘텐츠를 여기에 배치하십시오.
매개 변수 조합, 매개 변수 분석 및 기타 기능 포함
"""

class PromptMix:
    def __init__(self, **kwargs) -> None:
        self.prompt = kwargs.get("prompt", None)
        self.area = kwargs.get("area", None)
        self.quality = kwargs.get("quality", None)
        self.stylize = kwargs.get("stylize", None)
        self.seed = kwargs.get("seed", None)
        self.chaos = kwargs.get("chaos", None)
        self.image = kwargs.get("image", None)
        self.imageratio = kwargs.get("imageratio", None)
        self.version = kwargs.get("version", None)
        self.niji = kwargs.get("niji", None)        
        self.no = kwargs.get("no", "")
        self.style = kwargs.get("style", None)

    def BannedCheck(self):
        # 블랙리스트에 있는 키워드는 피드백을 제공합니다.
        if self.prompt and any((match := __banned) in self.prompt for __banned in BotSettings["BotParam"]["Banned_Word"]):
            return (False, "Has Banned Word:{}".format(match))

    def PromptClear(self, _prompt, splitstr = "--"):
        """
        检查用户输入의部分是否有链接 是否有自己输入의参数 是否有不合理의参数
        소개链接有效性 参数错误等等等等,加入对整体의代码性能有较大影响,在前端进行限制即可
        하지 말아야 할 것www开头의链接 是违禁词 会堵塞队列
        """
        # 링크 처리
        LinkPrompt = re.findall(r'https?://\S+', _prompt, flags=re.IGNORECASE)
        LinkStr = ""
        # 콘텐츠에서 적합한 링크를 복원하는 루프
        for _link in LinkPrompt:
            _prompt = _prompt.replace(_link, "")
            if _link.endswith(("jpg", "jpeg", "png", "gif", "bmp", "webp", "svg", "tiff", "ico")):
                LinkStr += "{} ".format(_link)
        
        # 콘텐츠 지우기niji
        _prompt = re.sub(r"--niji\s+\S*", "", _prompt)
        # 매개변수 처리, 사용자가 직접 입력한 일부 설정값으로 매개변수를 반환
        result = (lambda x: [x[:x.find(splitstr)].strip(), splitstr + x[x.find(splitstr) + len(splitstr):].strip()] if splitstr in x else False)(_prompt)
        if type(result) == list:
            _prompt = LinkStr + result[0]
            return _prompt, result[1]
        return _prompt, ""
        

    def DJPromptMix(self):
        self.BannedCheck()
        # Image + PromptWord + --no + --imageratio + --area + --quality + --stylize + --seed + --chaos + --niji + --version + PromptOption

        # Prompt 처리 중
        prompt, UserOpt = self.PromptClear(str(self.prompt))

        # 파라미터 핸들링
        try:
            ImageAdd = " {} ".format(self.image.url) if self.image and hasattr(self.image, 'url') and "http" in self.image.url else "" 
            prompt =  ImageAdd + prompt
        except Exception as e:
            return (False, "Error in PromptMix:{}".format(str(e)))

        prompt += " --no {} ".format(self.no) if self.no else ""
        prompt += " --iw {} ".format(round(((self.imageratio + 5) * 0.1), 1)) if (self.image or prompt.startswith("http")) and self.imageratio else ""
        prompt += " --quality {} ".format(self.quality) if self.quality and 0.25 < float(self.quality) < 2.0 else ""

        if self.area:
            if "：" in self.area: self.area = self.area.replace("：", ":")
            area_parts = self.area.split(":")
            if len(area_parts) == 2 and all(part.isdigit() for part in area_parts):
                area_num = int(area_parts[0]) / int(area_parts[1])
                prompt += " --ar {} ".format(self.area) if 0.5 < area_num < 2.0 and area_num != 1.0 else ""

        prompt += " --seed {} ".format(self.seed) if self.seed and 0 < self.seed < 4294967295 else ""
        prompt += " --niji {} ".format(self.niji) if self.niji else ""
        prompt += " --stylize {} ".format(self.stylize) if self.stylize and 0 < self.stylize < 1000 and self.niji != 4 else ""
        prompt += " --chaos {} ".format(self.chaos) if self.chaos else ""
        prompt += " --v {} ".format(self.version) if self.version else ""
        prompt += " --style raw " if self.style == False and self.version == "5.1" else ""
        prompt += UserOpt

        return (True, prompt)

