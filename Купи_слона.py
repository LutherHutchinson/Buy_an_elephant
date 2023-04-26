import logging

from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

Agree = ['ладно', 'куплю', 'покупаю', 'хорошо']


@app.route('/', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    if req['session']['new']:
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = [{"title": 'Отстань',
                                      "payload": {
                                          "text": 'Отстань'},
                                      "hide": True}]
        return
    else:
        if req["request"]["type"] == "SimpleUtterance":
            if req['request']['command'] in Agree:
                res['response']['text'] = 'ПРОДАНО!!!'
            else:
                res['response']['text'] = f'Все говорят {req["request"]["command"]}, а ты купи слона!'
        elif req["request"]["type"] == "ButtonPressed":
            res['response']['text'] = f'Все говорят {req["request"]["payload"]["text"]}, а ты купи слона!'
        else:
            res['response']['text'] = 'Так, купишь или нет?'
        return


if __name__ == '__main__':
    app.run()
