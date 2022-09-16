import datetime,sys
from rocketry import Rocketry
from rocketry.conditions.api import every, daily, time_of_day
from rocketry.conds import after_finish  # 完成某个任务后
from rocketry.args import Session  # 关闭用到

def get_data():
    print(datetime.datetime.now())
    print(sys._getframe().f_code.co_name)


app = Rocketry(config={'instant_shutdown': True}) # 加了参数表示关闭时候，终止正在运行的任务

time1 = daily.between('09:25', '09:30')
time2 = every('5 minute') & time_of_day.between('09:30', '09:40')
time3 = every('5 minute') & time_of_day.between('09:40', '11:30')
time4 = every('5 minute') & time_of_day.between('13:00', '15:00')
time5 = daily.after('15:00')

timeall = [time1, time2, time3, time4, time5]
for i, v in enumerate(timeall):
    app.task(v, func=get_data, name=str(i))

# 关闭的代码，这里的'4'是你要在某个程序运行完成后，对应上面的task里面的name，
# 如果使用修饰器方式，那么直接填写函数名
# 这里也可以写定时关闭
@app.task(after_finish('4'), execution="thread")
def do_shutdown(session=Session()):
    session.shutdown()

if __name__ == '__main__':
    app.run()
