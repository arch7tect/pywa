import logging
import flask  # pip3 install flask
import googletrans  # pip3 install googletrans==4.0.0-rc1
from pywa import WhatsApp, filters
from pywa.types import Message, SectionList, CallbackSelection, Section, SectionRow

flask_app = flask.Flask(__name__)
translator = googletrans.Translator()

wa = WhatsApp(
    phone_id='247666181773936',
    token='EAANpSTSV5EABOZB7dBIwsnJqXDQLfZCnZC9nomASltvwwjc3EAThPXznHZCZBu8tPeAGFZCk9gGBiFreNOUGDSrSkIfyQ2Dti7rrZCcJ86ZCg1a2oYAAmxBoXPC3tLnadJI5UrbUZBQewLk75CQ8nhfZAYcYvVld8bQoHZA19VZACXZA1YV2WAYrI7beAd7dsZARl51uoA',
    server=flask_app,
    verify_token='038726584673',
    callback_url='https://still-kindly-chigger.ngrok-free.app',
    app_id=960188065899584,
    app_secret='dd6427d4b6c49b3b5bd2742818e84927',
)

MESSAGE_ID_TO_TEXT: dict[str, str] = {}  # msg_id -> text
POPULAR_LANGUAGES = {
    "en": ("English", "🇺🇸"),
    "es": ("Español", "🇪🇸"),
    "fr": ("Français", "🇫🇷")
}
OTHER_LANGUAGES = {
    "iw": ("עברית", "🇮🇱"),
    "ar": ("العربية", "🇸🇦"),
    "ru": ("Русский", "🇷🇺"),
    "de": ("Deutsch", "🇩🇪"),
    "it": ("Italiano", "🇮🇹"),
    "pt": ("Português", "🇵🇹"),
    "ja": ("日本語", "🇯🇵"),
}


@wa.on_message(filters.text)
def offer_translation(_: WhatsApp, msg: Message):
    msg_id = msg.reply_text(
        text='Choose language to translate to:',
        buttons=SectionList(
            button_title='🌐 Choose Language',
            sections=[
                Section(
                    title="🌟 Popular languages",
                    rows=[
                        SectionRow(
                            title=f"{flag} {name}",
                            callback_data=f"translate:{code}",
                        )
                        for code, (name, flag) in POPULAR_LANGUAGES.items()
                    ],
                ),
                Section(
                    title="🌐 Other languages",
                    rows=[
                        SectionRow(
                            title=f"{flag} {name}",
                            callback_data=f"translate:{code}",
                        )
                        for code, (name, flag) in OTHER_LANGUAGES.items()
                    ],
                ),
            ]
        )
    )
    # Save the message ID so we can use it later to get the original text.
    MESSAGE_ID_TO_TEXT[msg_id] = msg.text

@wa.on_callback_selection(filters.startswith('translate:'))
def translate(_: WhatsApp, sel: CallbackSelection):
    lang_code = sel.data.split(':')[-1]
    try:
        # every CallbackSelection has a reference to the original message (the selection's message)
        original_text = MESSAGE_ID_TO_TEXT[sel.reply_to_message.message_id]
    except KeyError:  # If the bot was restarted, the message ID is no longer valid.
        sel.react('❌')
        sel.reply_text(
            text='Original message not found. Please send a new message.'
        )
        return
    try:
        translated = translator.translate(original_text, dest=lang_code)
    except Exception as e:
        sel.react('❌')
        sel.reply_text(
            text='An error occurred. Please try again.'
        )
        logging.exception(e)
        return

    sel.reply_text(
        text=f"Translated to {translated.dest}:\n{translated.text}"
    )


# Run the server
flask_app.run(port=8080, debug=True)
