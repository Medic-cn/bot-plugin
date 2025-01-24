from event_build import send, send_template, Message, PressButtonEvent, Event
from activity import Activity
from datetime import timedelta

P_NAME = "游戏测试1" # 游戏名/插件名

class Main(Activity): # 常规方法 在event_in中逐一处理逻辑
    def __init__(self, uuid, message:Message):
        self.live_period = timedelta(minutes=1)
        super().__init__(uuid)
        send(
            message=message,
            text="你开启了一个测试用activity。现在请你按下PressA进行输入测试。"
        )
        self.next_button = "PressA"
        self.last_obj = message

    def message_in(self, message:Message):
        self.last_obj = message # 记录最后一个可用对象以进行回复
        self._relive() # 调用一次会自动续期以延长存活时间
        send(
            message=message,
            text="你传入了消息。但我们希望你按下按钮。"
        )
    
    def event_in(self, event:PressButtonEvent):
        self.last_obj = event # 记录最后一个可用对象以进行回复
        self._relive() # 调用一次会自动续期以延长存活时间
        if event.button_name == self.next_button:
            if self.next_button == "PressA":
                self.next_button = "PressB"
            elif self.next_button == "PressB":
                self.next_button = "PressC"
            elif self.next_button == "PressC":
                self.next_button = "PressX"
            elif self.next_button == "PressX":
                self.next_button = "PressY"
            else:
                send(
                    event=event,
                    text="你已完成按键测试。本事件将立即销毁。"
                )
                self.status = -2 # 状态码变更为-2时 会自动注销
                return
            send(
                event=event,
                text=f"你做的很棒，下一步你需要按下{self.next_button}"
            )
        else:
            send(
                event=event,
                text=f"你按下了{event.button_name}，这是错误的。你需要按下{self.next_button}"
            )
    def live_time_over(self):
        obj = self.last_obj # 总是回复最后获得的事件/消息 避免消息超时无法回复
        text = "本测试ACT超时未续期，现在自动销毁中"
        if isinstance(obj, Message):
            send(message=obj,text=text)
        elif isinstance(obj, Event):
            send(event=obj,text=text)
        return super().live_time_over()