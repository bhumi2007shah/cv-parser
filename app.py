from flask import Flask, Response, request
from flask import jsonify

from ParseResume import parseResume

from services.FileService import convert_to_text

app = Flask(__name__)


@app.route("/parsecv", methods=['GET'])
def parsecv():
    return Response(parseResume(), mimetype="application/json")


@app.route("/textconvert", methods=['GET'])
def textconvert():
    fileUrl = request.args.get("fileUrl")
    return Response(convert_to_text(fileUrl), mimetype="text/plain", )


if __name__ == "__main__":
    app.run()
