import flask  # pip3 install flask
from pywa import WhatsApp
from pywa.types import Message

flask_app = flask.Flask(__name__)

wa = WhatsApp(
    phone_id='247666181773936',
    token='EAANpSTSV5EABOZB7dBIwsnJqXDQLfZCnZC9nomASltvwwjc3EAThPXznHZCZBu8tPeAGFZCk9gGBiFreNOUGDSrSkIfyQ2Dti7rrZCcJ86ZCg1a2oYAAmxBoXPC3tLnadJI5UrbUZBQewLk75CQ8nhfZAYcYvVld8bQoHZA19VZACXZA1YV2WAYrI7beAd7dsZARl51uoA',
    server=flask_app,
    verify_token='038726584673',
    callback_url='https://still-kindly-chigger.ngrok-free.app',
    app_id=960188065899584,
    app_secret='dd6427d4b6c49b3b5bd2742818e84927',
)

@wa.on_message()
def hello(_: WhatsApp, msg: Message):
    msg.react('👋')
    msg.reply(f'Hello {msg.from_user.name}!')

# Run the server
flask_app.run(port=8080, debug=True)

