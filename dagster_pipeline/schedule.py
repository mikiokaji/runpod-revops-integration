from dagster import schedule
from dagster_pipeline.runpod_revops_pipeline import runpod_revops_pipeline

# Every minute schedule
@schedule(cron_schedule="* * * * *", job=runpod_revops_pipeline, execution_timezone="America/Chicago")
def every_minute_schedule(_context):
    return {}

# Every 5 minutes schedule
@schedule(cron_schedule="*/5 * * * *", job=runpod_revops_pipeline, execution_timezone="America/Chicago")
def every_five_minutes_schedule(_context):
    return {}

# Every hour schedule
@schedule(cron_schedule="0 * * * *", job=runpod_revops_pipeline, execution_timezone="America/Chicago")
def every_hour_schedule(_context):
    return {}