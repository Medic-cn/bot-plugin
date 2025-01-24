from event_build import send, send_template, Message, PressButtonEvent, Event
from activity import Activity
from datetime import timedelta

from logger import log
from datetime import datetime
import random

P_NAME = "木鱼" # 游戏名/事件名 (如果是游戏就用/游戏 游戏名 触发游戏,否则在代码内调用并启动)
P_AUTHOR = "susu" # 作者名 在此署名后会在游戏启动时发送出去 或在游戏列表内显示

class Main(Activity): 
    def __init__(self, uuid, message:Message):
        self.live_period = timedelta(minutes=1)
        super().__init__(uuid)
        send_template(
            temp_name="woodenfish_start",
            message=message
        )

        self.last_obj = message
        self.count = 0
        self.start_time = datetime.now()

    def message_in(self, message:Message):
        self.last_obj = message # 记录最后一个可用对象以进行回复
        self._relive() # 调用一次会自动续期以延长存活时间
    
    def event_in(self, event:PressButtonEvent):
        self.last_obj = event # 记录最后一个可用对象以进行回复
        self._relive() # 调用一次会自动续期以延长存活时间
        self._on_click(event=event)

    def _on_click(self, event:PressButtonEvent):
        self.count +=1
        temp_name = random.choice(["woodenfish_click1", "woodenfish_click2"])
        log("敲打了一次木鱼","warn")
        event.auto_delete = True
        send_template(
            event=event,
            temp_name=temp_name,
            markdown_args={
                "text1":f"累计功德：{self.count}",
                "text2":f"累计时间：{self._format_seconds((datetime.now() - self.start_time).total_seconds())}"
            }
        )

    def _format_seconds(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        result = ""
        
        if hours > 0:
            result += f"{int(hours)}小时"
        if minutes > 0:
            result += f"{int(minutes)}分钟"
        if seconds > 0 or result == "":  # 如果时间为 0 秒，输出 "0秒"
            result += f"{int(seconds)}秒"
        
        return result

    def live_time_over(self):
        obj = self.last_obj
        obj.auto_delete = False
        text = f"木鱼时间结束\n累计功德：{self.count}\n累计时间：{self._format_seconds((datetime.now() - self.start_time).total_seconds())}"
        if isinstance(obj, Message):
            send(message=obj,text=text)
        elif isinstance(obj, Event):
            send(event=obj,text=text)
        return super().live_time_over()