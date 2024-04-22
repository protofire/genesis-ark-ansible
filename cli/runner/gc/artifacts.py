import os
from datetime import datetime
from runner.logging import logger


def days_between(d1, d2):
    return abs((d2 - d1).days)


def is_empty(dir_path):
    dir_contents = os.listdir(dir_path)
    return len(dir_contents) == 0


def delete_dir(dir):
    dir_path = dir[0]
    subdir_names = dir[1]
    file_names = dir[2]

    # Remove files
    for file_name in file_names:
        file_path = os.path.join(dir_path, file_name)
        if os.path.exists(file_path):
            logger.info(f"remove file: path = '{file_path}'")
            os.remove(file_path)

    # Remove subdirectories
    for subdir_name in subdir_names:
        subdir_path = os.path.join(dir_path, subdir_name)
        # Remove if path exists and empty
        if os.path.exists(subdir_path) and is_empty(subdir_path):
            logger.info(f"remove subdirectory: path = '{subdir_path}'")
            os.removedirs(subdir_path)

    # Remove parent directory
    if os.path.exists(dir_path) and is_empty(dir_path):
        logger.info(f"remove parent directory: path = '{dir_path}'")
        os.removedirs(dir_path)


def rotate_artifacts(max_age_days: int) -> None:
    now = datetime.now()

    jobs_dir_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "ansible", "jobs")
    )

    logger.info(f"jobs_dir_path: path = '{jobs_dir_path}'")

    for job_dir in os.walk(jobs_dir_path, topdown=False):
        job_dir_path = job_dir[0]

        # skip current path if it's a root jobs direcory
        if job_dir_path == jobs_dir_path:
            logger.info(f"skip root directory: path = '{job_dir_path}'")
            continue

        # skip current path is it has already been deleted
        if not os.path.exists(job_dir_path):
            logger.warning(f"path already deleted: path = '{job_dir_path}'")
            continue
        updated_at_ts = os.stat(job_dir_path).st_mtime
        updated_at = datetime.fromtimestamp(updated_at_ts)
        if days_between(now, updated_at) >= max_age_days:
            delete_dir(job_dir)
