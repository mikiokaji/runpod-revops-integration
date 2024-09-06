from dagster import repository
from runpod_revops_pipeline import runpod_revops_pipeline
from schedule import every_minute_schedule, every_five_minutes_schedule, every_hour_schedule

@repository
def runpod_revops_repo():
    return [runpod_revops_pipeline, every_minute_schedule, every_five_minutes_schedule, every_hour_schedule]