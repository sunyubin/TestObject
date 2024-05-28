import threading
import time

import common.Dobot.DoBotArm as Dbt


class Dobot:
    def __init__(self, homeX, homeY, homeZ, homeR=0, portName="COM5"):
        self.homeX = homeX
        self.homeY = homeY
        self.homeZ = homeZ
        self.homeR = homeR
        self.portName = portName
        self.ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ, homeR, portName)

    def moveArmXY(self, x, y, waitTime=0):  # 移动坐标
        self.ctrlBot.moveArmXY(x, y)
        time.sleep(waitTime)

    def pickToggle(self, x, waitTime=0):  # 上下点击
        self.ctrlBot.pickToggle(x)
        time.sleep(waitTime)

    def moveHome(self, waitTime=0):  # 回到原点
        self.ctrlBot.moveHome()
        time.sleep(waitTime)

    def toggleSuction(self):  # 使用外设
        self.ctrlBot.toggleSuction()
