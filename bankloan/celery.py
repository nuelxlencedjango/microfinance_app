import os
from celery import Celery
#from celery.schedule import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bankloan.settings")
app = Celery("bankloan")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()





app.conf.beat_schedule ={
    'every-60 minute':{
        'task':'loanApp.tasks.check_due_date',
        'schedule':60,
        #'args': ''
        #'args': (16, 16)
        #'args':('nuel4xelence@gmail.com',)
        }
}



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')





