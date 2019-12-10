from flask import Flask, Response, request
from ParseResume import parseResume
from config import config

from services.FileService import convert_to_text


def create_app():
    print(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object('config')

    @app.route("/parsecv", methods=['GET'])
    def parsecv():
        fileName = request.args.get("file")
        return Response(parseResume(fileName), mimetype="application/json")

    @app.route("/textconvert", methods=['GET'])
    def textconvert():
        fileName = request.args.get("file")
        return Response(convert_to_text(fileName), mimetype="text/plain", )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)