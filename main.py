import subprocess
from logging import config, getLogger

from bottie import Bottie


LOG_CONFIG_PATH = "config/logging_config.ini"

# Configure the logger using the configuration file
config.fileConfig(LOG_CONFIG_PATH)

# Create a logger
logger = getLogger(__name__)


def get_git_version():
    try:
        command = ["git", "describe", "--tags", "--always"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logger.warning(
                f"Failed to retrieve Git version. Error: {result.stderr.strip()}"
            )
    except FileNotFoundError:
        logger.warning("Git command not found. Unable to retrieve Git version.")
    return None


def main():
    # Log the Git version
    git_version = get_git_version()
    if git_version:
        logger.info(f"Welcome to Bottie ({git_version}). Lets begin...")
    else:
        logger.info("Welcome to Bottie. Lets begin...")

    bottie = Bottie()

    bottie.run()


if __name__ == "__main__":
    main()
