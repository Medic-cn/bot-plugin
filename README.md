*Ciallo～(∠・ω ∠ )⌒★*
# 丛雨丸bot插件开发仓库
这里存放丛雨丸bot游戏功能的插件代码以及一些模拟真实环境的工具🛠️

(目前还在缓慢完善中...欢迎帮助完善bot游戏功能)

[丛雨丸Bot交流群🎇：429379849](https://qbot.nappig.com/qbot/group)
***
## 目录结构
> - main.py # 开发工具主代码
> - plugins
>   - __init__.py # 初始化插件代码
>   - game_test1.py # 示例游戏代码：按钮测试（回调型）
>   - game_test2.py # 示例游戏代码：按钮测试（阻断型）
>   - wooden_fish.py # 示例游戏代码：木鱼 （回调型）
>   - ... # 更多游戏期待更新 或期待你的贡献
***
**让我们开始✨**
## 框架说明
> Python纯手搓框架，由Activity系统驱动游戏运行
> 
> 在这套系统里，触发特定事件会启动Activity，从而长时间储存事件状态以及执行定时等任务
>
> 例如 使用指令“/游戏 xx”，就会启动名为xx的游戏Activity
>
> 每当有新的消息或按钮事件都会通过函数回调传入并处理（可能需要过滤无用消息）

## 运作流程
### 1.结构
每个插件（.py文件）为一个Activity的封装。

每个插件内的`Main`对象为一个Activity。插件只是对该对象进行封装。

每个插件内的`P_NAME`常量，为该Activity的名字。根据名字可启动对应Activity。

**意思是：丢一个py文件就是一个插件了，文件里的Main类就是Activity**
### 2.初始化Activity
每当启动Activity时，都会调用`Main`对象的`__init__`函数，并传入`uuid`和`message`对象
> uuid: 用户/群聊的唯一标识，
> 
> message：一个消息对象。包含收到触发启动Activity时的原始消息数据

在初始化Activity时，可以对该对象设定一些初始值数据，以便接下来运行时使用

### 3.接收消息/事件
初始化完成后，机器人收到的所有消息都会回调到`message_in`和`event_in`函数，分别接收消息和事件

例如，当有人发送`@丛雨丸 开始游戏`时，`message_in`会收到这个消息回调

例如，当有人按下回调按钮时，`event_in`会收到这个按钮的回调事件

### 4.续活
每个Activity都有超时时间。超时后，系统会调用`live_time_over`函数，然后销毁Activity

默认超时时间为3分钟，你可以在初始化时先修改父类的超时时间，例如
```python
self.live_period = timedelta(minutes=1)
super().__init__(uuid) # 初始化父类
```

在Activity运行时，也可以通过续活来延长存活时间：
```python
self._relive() # 调用一次的续活时间为self.live_period
```
### 5.阻塞法！
普通Activity只会在每次有回调时运行，每次收到回调都要重新读取self的数据再处理。

**而阻塞法可以让Activity一直运行，不需要回调**

阻塞法的Activity作为独立的线程运行，只要使用函数来等待事件/按钮传入即可

例如：
```python
button = self.wait_for_button()```
这样，Activity就会卡在这里，直到有按钮被按下才会继续运行。

**也可以指定监听特定按钮和设定超时时间**
```python
event = self.wait_for_button("PressA", timeout=60)  # 等待被按下"PressA"按钮，超时时间 60 秒
```
这样，只会监听指定按钮按下。当60秒内无人按下时，返回None

（其实还可以指定按下的人等等）

## 特有对象：
```python
class Message:
    type:str # 群聊：group / 私聊：private / 频道：channel
    content:str # 收到的消息文字
    sender_uid:str # 发送者ID
    group_id:str # 群聊ID，频道为频道的id
    time:datetime # 消息发送时间

class PressBottonEvent(Event):
    type:str # 同上
    group_id:str # 同上
    user_id:str # 按下按钮的用户ID
    button_name:str # 按下的按钮名
