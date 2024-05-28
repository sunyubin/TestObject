import threading
import DoBotArm as Dbt

#Example of bundling functions
def functons():
    homeX, homeY, homeZ = 250, 0, 50
    ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ) #Create DoBot Class Object with home position x,y,z
    print("moveArmXY(250, 100)")
    # ctrlBot.moveArmXY(250, 100)
    ctrlBot.moveArmXY(250, 100)
    print("pickToggle(-40)")
    ctrlBot.pickToggle(-40)
    print("pickToggle(-40)")
    ctrlBot.pickToggle(-40)
    print("moveHome()")
    ctrlBot.moveHome()
    print("pickToggle(-40)")
    ctrlBot.pickToggle(-40)
    print("toggleSuction")
    ctrlBot.toggleSuction()
    print("pickToggle(-40)")
    ctrlBot.pickToggle(-40)



if __name__ == '__main__':
    functons()