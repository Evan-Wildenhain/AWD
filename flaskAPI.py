from flask import Flask
from flask import request
from addon import searchVideo
app = Flask(__name__)


@app.route("/request", methods=['GET'])
def request_dictionary():
    url = request.args.get('url')
    word_dict, timestamps = searchVideo("https://www.youtube.com/watch?v=iuslUzbJEaw")
    return word_dict


if __name__ == '__main__':
    app.run(debug=True)