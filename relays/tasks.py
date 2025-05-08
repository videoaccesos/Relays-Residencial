import os
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger
from config import CONFIG
from device_manager import RelayDevice
from models import SessionLocal, Log

WATCHDOG_INTERVAL=int(os.getenv('WATCHDOG_INTERVAL','60'))
WATCHDOG_THRESHOLD=int(os.getenv('WATCHDOG_THRESHOLD','120'))

def schedule_auto_off(sched,user,res_id,relay_id,duration):
    run_at=datetime.utcnow()+timedelta(seconds=duration)
    sched.add_job(id=f"off_{res_id}_{relay_id}_{int(run_at.timestamp())}",
                  func=execute_off,trigger=DateTrigger(run_date=run_at),
                  args=[user,res_id,relay_id],replace_existing=True)

def execute_off(user,res_id,relay_id):
    cfg=next(r for r in CONFIG['residences'] if r['id']==res_id)
    dev=RelayDevice(cfg); result_off=dev.set_and_get_states(relay_id,0)
    db=SessionLocal(); db.add(Log(user=user,residence_id=res_id,relay_id=relay_id,
                                  action='OFF',duration=0,result=str(result_off)))
    db.commit(); db.close()

def health_check():
    for res in CONFIG['residences']:
        try: RelayDevice(res).set_and_get_states(res['relays'][0]['id'],res['relays'][0]['id']); status='OK'; msg=''
        except Exception as e: status='ERROR'; msg=str(e)
        db=SessionLocal(); db.add(Log(user='watchdog',residence_id=res['id'],relay_id=-1,
                          action='PING',duration=0,result=f"{status}: {msg}"))
        db.commit(); db.close()
