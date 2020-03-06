import json

from flask import Flask, Response, request, jsonify

from CustomException.CustomException import CustomWebException
from ParseResume import parseResume
from config import config
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from services.FileService import convert_to_text


def create_app():
    if config.SENTRY_DSN is not None:
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            integrations=[FlaskIntegration()]
        )

    logging.basicConfig(filename="logs/cvparser.log", filemode="a+", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

    app = Flask(__name__)
    app.config.from_object('config')

    # Registering error handlers for application

    @app.errorhandler(CustomWebException)
    def web_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.route("/parsecv", methods=['GET'])
    def parsecv():
        fileName = request.args.get("file")
        return Response(parseResume(fileName), mimetype="application/json")

    @app.route("/textconvert", methods=['GET'])
    def textconvert():
        fileName = request.args.get("file")
        logging.info("Received request to extract text for file : " + fileName)
        return Response(convert_to_text(fileName), mimetype="text/plain")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=config.PORT, debug=True)
    logging.info('Started app in ' + config.APP_ENV + 'environment')
