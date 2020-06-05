from flask import Flask, jsonify

from CustomException.CustomException import CustomWebException
from config import config
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from controller.JdProcessController import jd_process_api
from controller.CvProcessController import cv_process_api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(jd_process_api)
    app.register_blueprint(cv_process_api)

    if config.SENTRY_DSN is not None:
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            integrations=[FlaskIntegration()]
        )

    # formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    #
    # handler = TimedRotatingFileHandler('logs/cvparser.log',
    #                                    when='midnight',
    #                                    backupCount=1)
    #
    # handler.setFormatter(formatter)
    # logger = logging.getLogger(__name__)
    # logger.addHandler(handler)

    logging.basicConfig(filename="logs/cvparser.log", filemode="a+", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

    app.config.from_object('config')

    @app.errorhandler(CustomWebException)
    def web_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        logging.info(response)
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=config.PORT, debug=True)
    logging.info('Started app in ' + config.APP_ENV + 'environment')
