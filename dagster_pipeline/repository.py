import logging
from dagster import repository
from dagster_pipeline.runpod_revops_pipeline import runpod_revops_pipeline
from schedule import every_minute_schedule, every_five_minutes_schedule, every_hour_schedule

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@repository
def runpod_revops_repo():
    logger.info("Initializing the RunPod RevOps repository.")
    return [runpod_revops_pipeline, every_minute_schedule, every_five_minutes_schedule, every_hour_schedule]