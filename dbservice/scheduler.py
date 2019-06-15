from apscheduler.schedulers.blocking import BlockingScheduler
import worker

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour='0,6,12,18')
def scheduled_job():
    worker.main()


sched.start()
