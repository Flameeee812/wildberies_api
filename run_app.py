import logging

from app import app
import logger


if __name__ == "__main__":

    logger.setup_logger()
    app_logger = logging.getLogger("run_app")

    try:
        app.logger.disabled = True

        app.run(port=5001, debug=True)
        app_logger.info("Соединение с сайтом открыто")

    except KeyboardInterrupt:
        app_logger.info("Соединение с сайтом закрыто")
