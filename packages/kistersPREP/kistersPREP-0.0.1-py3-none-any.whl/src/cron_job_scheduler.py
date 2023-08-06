"""the logic that parses the properties file and creates jobs for each cron entry"""
import glob
import os
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import config_parser

_MODEL_FILE_PATH = "../ml_models/*.py"


def start_scheduler():
    files_dict = _retrieve_model_file_paths()
    config = config_parser.read_properties(files_dict.keys())

    scheduler = BlockingScheduler()
    _add_jobs_to_scheduler(scheduler, config, files_dict)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def _retrieve_model_file_paths():
    """
    Accessing all python files in /ml_models/ folder.
    Returns dict of file names and relative file paths, e.g. {"example_model": "../../ml_models/example_model.py"}.
    """
    name_path_dict = dict()
    for file in glob.glob(_MODEL_FILE_PATH):
        file_name_py = os.path.basename(file)
        name = os.path.splitext(file_name_py)
        name_path_dict[name[0]] = file

    return name_path_dict


def _add_jobs_to_scheduler(scheduler, config, files_dict):
    for ml_script in files_dict.keys():
        cron_expression = config[ml_script][ml_script + ".cron_expression"]
        trigger = CronTrigger.from_crontab(cron_expression)
        scheduler.add_job(_run_script, trigger, args=[files_dict[ml_script]])
        print('Added script: ' + ml_script + ', cron: ' + cron_expression)


def _run_script(script_name):
    subprocess.call("python3 " + script_name, shell=True)
