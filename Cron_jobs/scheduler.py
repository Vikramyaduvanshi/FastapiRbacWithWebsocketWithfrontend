
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Cron_jobs.jobs import cronejob
from Database.ds import SessionLocal

scheduler = AsyncIOScheduler()


async def run_signal_checker():

    db = SessionLocal()

    try:

        await cronejob(db)

    finally:

        db.close()


def start_scheduler():
    scheduler.add_job(run_signal_checker, "interval", seconds=30  )
    scheduler.start()

    print("start sheduler")