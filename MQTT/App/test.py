import schedule
import time
import datetime

def job():
    print("I'm working...")
    with open('dateInfo.txt','a') as outFile:
        outFile.write('\n' + str(datetime.datetime.now()))

schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
# 
#
# Company/home/bagues/RDC/SDB/shower
#
# {"debit":"0","time":"2018-03-16T11:08:19.187Z"}
