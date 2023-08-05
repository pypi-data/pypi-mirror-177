import os
IS_PRODUCTION = os.environ.get("ENV") == "production"
IS_DEVELOPMENT = not IS_PRODUCTION
IS_DIGITAL_OCEAN = os.environ.get("IS_DIGITAL_OCEAN") == 'True'


def is_docker():
    path = '/proc/self/cgroup'

    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
        or os.environ.get('KUBERNETES_SERVICE_HOST') is not None
    )


IS_DOCKER = is_docker()

TARGET_DIR = "production" if IS_PRODUCTION else "test"

TARGET_DIR_PARENT = 'digital-ocean-app-data' if IS_DIGITAL_OCEAN else 'app-data'
BASE_PATH = f'{TARGET_DIR_PARENT}/{TARGET_DIR}'
PROFILES_PATH = f'{BASE_PATH}/profiles'
SCREENSHOTS_PATH = f'{BASE_PATH}'

LOGS_PATH = f'../{BASE_PATH}/debug'

DB_PATH = f'{BASE_PATH}/app-data.db'

TARGET_USERS_INPUT_PATH = f'udemy_gather_data/{TARGET_DIR}/input_data/target-users.json'

TARGET_USERS_OUTPUT_PATH = f"udemy_gather_data/{TARGET_DIR}/output_data/target_users.json"
TARGET_COURSES_OUTPUT_PATH = f"udemy_gather_data/{TARGET_DIR}/output_data/target-courses.json"

SEED_DB_TARGET_USERS = TARGET_USERS_OUTPUT_PATH
SEED_DB_ALL_USERS = f"udemy_gather_data/{TARGET_DIR}/output_data/all-users.json"

SEED_DB_TARGET_COURSES = TARGET_COURSES_OUTPUT_PATH
SEED_DB_ALL_COURSES = f"udemy_gather_data/{TARGET_DIR}/output_data/all-courses.json"

K8_JOB_YAML = f'../k8s/jobs/udemy-bot-job.yaml'
DOCKER_COMPOSE_YAML = f'docker-compose.yaml'
DOCKER_COMPOSE_YAML_FOR_VIDEOS = f'composes'
ACTIONS_PATH = f'udemy_gather_data/{TARGET_DIR}/output_data/actions.txt'
WAIT_DURATION = 20
WAIT_DURATION_SHORT = 10
WAIT_DURATION_VERY_SHORT = 5


RETRY_ATTEMPTS_LOW = 3
RETRY_ATTEMPTS_HIGH = 5

SECONDS_IN_MINUTES = 60