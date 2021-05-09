import logging
import time
from datetime import (
    datetime,
    timedelta,
    )

from plotmanager.library.parse.configuration import get_config_info
from plotmanager.library.utilities.jobs import (
    has_active_jobs_and_work,
    load_jobs,
    monitor_jobs_to_start,
    )
from plotmanager.library.utilities.log import check_log_progress
from plotmanager.library.utilities.processes import get_running_plots

conf = get_config_info()

logging.basicConfig(
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=conf.debug_level
    )

logging.info(f'Debug Level: {conf.debug_level}')
logging.info(f'Chia Location: {conf.chia_location}')
logging.info(f'Log Directory: {conf.log_directory}')
logging.info(f'Jobs: {conf.jobs}')
logging.info(f'Manager Check Interval: {conf.manager_check_interval}')
logging.info(f'Max Concurrent: {conf.max_concurrent}')
logging.info(f'Progress Settings: {conf.progress_settings}')
logging.info(f'Notification Settings: {conf.notification_settings}')
logging.info(f'View Settings: {conf.view_settings}')

logging.info(f'Loading jobs into objects.')
jobs = load_jobs(conf.jobs)

next_log_check = datetime.now()
next_job_work = {}
running_work = {}

logging.info(f'Grabbing running plots.')
jobs, running_work = get_running_plots(jobs, running_work)
for job in jobs:
    max_date = None
    for pid in job.running_work:
        work = running_work[pid]
        start = work.datetime_start
        if not max_date or start > max_date:
            max_date = start
    if not max_date:
        continue
    next_job_work[job.name] = max_date + timedelta(minutes=job.stagger_minutes)
    logging.info(f'{job.name} Found. Setting next stagger date to {next_job_work[job.name]}')

logging.info(f'Starting loop.')
while has_active_jobs_and_work(jobs):
    # CHECK LOGS FOR DELETED WORK
    logging.info(f'Checking log progress..')
    check_log_progress(
        jobs=jobs, running_work=running_work, progress_settings=conf.progress_settings,
        notification_settings=conf.notification_settings, view_settings=conf.view_settings
        )
    next_log_check = datetime.now() + timedelta(seconds=conf.manager_check_interval)

    # DETERMINE IF JOB NEEDS TO START
    logging.info(f'Monitoring jobs to start.')
    jobs, running_work, next_job_work, next_log_check = monitor_jobs_to_start(
        jobs=jobs,
        running_work=running_work,
        max_concurrent=conf.max_concurrent,
        next_job_work=next_job_work,
        chia_location=conf.chia_location,
        log_directory=conf.log_directory,
        next_log_check=next_log_check,
        )

    logging.info(f'Sleeping for {conf.manager_check_interval} seconds.')
    time.sleep(conf.manager_check_interval)
