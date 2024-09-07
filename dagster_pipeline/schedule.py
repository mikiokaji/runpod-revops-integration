import logging
from dagster import schedule
from dagster_pipeline.runpod_revops_pipeline import runpod_revops_pipeline

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Every minute schedule
@schedule(cron_schedule="* * * * *", job=runpod_revops_pipeline, execution_timezone="America/Chicago")
def every_minute_schedule(_context):
    logger.info("Triggered every_minute_schedule.")
    return {}

# Every 5 minutes schedule
@schedule(cron_schedule="*/5 * * * *", job=runpod_revops_pipeline, execution_timezone="America/Chicago")
def every_five_minutes_schedule(_context):
    logger.info("Triggered every_five_minutes_schedule.")
    return {}

# Every hour schedule
@schedule(cron_schedule="0 * * * *", job=runpod_revops_pipeline, execution_timezone="America/Chicago")
def every_hour_schedule(_context):
    logger.info("Triggered every_hour_schedule.")
    return {}