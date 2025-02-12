import time
import logging
from datetime import datetime, timedelta, timezone
from backend.models import RequestLog
from backend.database import db
from celery.result import AsyncResult

logger = logging.getLogger(__name__)

def monitor_running_tasks(app, check_interval=10, timeout_threshold=20):
    """
    Periodically checks tasks with status "Running" or "Pending" (in RequestLog).
    If a task's heartbeat (last_updated timestamp) is older than `timeout_threshold`
    seconds or if the corresponding Celery task shows an updated state, update the DB.
    """
    while True:
        with app.app_context():
            now = datetime.now(timezone.utc)
            # Get all RequestLog records that are still not final.
            tasks_to_check = RequestLog.query.filter(
                RequestLog.status.in_(["Pending", "Running"])
            ).all()
            tasks_updated = False

            for task in tasks_to_check:
                # Use 'last_updated' if available; fallback to 'timestamp'
                # Using `or` ensures that if last_updated is None, task.timestamp is used.
                last_update = getattr(task, 'last_updated', None) or task.timestamp

                # If no valid timestamp is available, log a warning and skip this task.
                if last_update is None:
                    logger.warning(f"Task {task.id} has no valid timestamp or last_updated value. Skipping heartbeat check.")
                    continue

                # Ensure last_update is timezone-aware. If it's naive, assume UTC.
                if last_update.tzinfo is None:
                    last_update = last_update.replace(tzinfo=timezone.utc)

                # Check if the task's heartbeat is older than the threshold.
                if now - last_update > timedelta(seconds=timeout_threshold):
                    # Only update if not already aborted.
                    if task.status != "Aborted":
                        task.status = "Aborted"
                        if task.options and isinstance(task.options, dict):
                            task.options["auto_abort_reason"] = "No heartbeat detected. Task auto-aborted."
                        logger.info(f"Task {task.id} auto-aborted due to inactivity. Last updated: {last_update}")
                        tasks_updated = True

                # If a Celery task ID is present, check its current state.
                celery_task_id = getattr(task, 'celery_task_id', None)
                if celery_task_id:
                    celery_result = AsyncResult(celery_task_id)
                    if celery_result.state != task.status:
                        logger.info(f"Task {task.id} status updated from {task.status} to {celery_result.state} based on Celery result.")
                        task.status = celery_result.state
                        if celery_result.state in ['SUCCESS', 'FAILURE']:
                            task.result = celery_result.result
                        tasks_updated = True

            if tasks_updated:
                db.session.commit()

        time.sleep(check_interval)
