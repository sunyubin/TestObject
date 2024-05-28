import datetime


def time_now():
    current_time = datetime.datetime.now()
    time_now_Y = current_time.strftime('%Y')
    time_now_m = current_time.strftime('%m')
    time_now_D = current_time.strftime('%d')
    time_now_H = current_time.strftime('%H')
    time_now_M = current_time.strftime('%M')
    time_now_S = current_time.strftime('%S')
    time_now_Day = current_time.strftime('%Y_%m_%d')
    time_now_Time = current_time.strftime('%H:%M:%S')
    formatted_time = current_time.strftime("%Y_%m_%d_%H_%M")
    return time_now_Y, time_now_m, time_now_D, time_now_H, time_now_M, time_now_S, time_now_Day, time_now_Time, formatted_time
