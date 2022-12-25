import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message

load_dotenv()
machines = {}

def create_machine():
    machine = TocMachine(
        states=[
            'user', 'init',
            'chat', 'conversation',
            'edit_text', 'get_writing',
            'edit_code', 'get_code', 'get_inst',
            'generate_image', 'create_image' 
        ],
        transitions=[
            {'trigger': 'advance', 'source':'user', 'dest':'init', 'conditions':'is_going_to_init'},
            {'trigger': 'advance', 'source':'init', 'dest':'chat', 'conditions':'is_going_to_chat'},
            {'trigger': 'advance', 'source':'conversation', 'dest':'conversation', 'conditions':'is_going_in_conversation'},
            {'trigger': 'advance', 'source':'chat', 'dest':'conversation', 'conditions':'is_going_in_conversation'},
            {'trigger': 'advance', 'source':'init', 'dest':'edit_text', 'conditions':'is_going_to_edit_text'},
            {'trigger': 'advance', 'source':'edit_text', 'dest':'get_writing', 'conditions':'is_going_to_get_writing'},
            {'trigger': 'advance', 'source':'get_writing', 'dest':'get_writing', 'conditions':'is_going_to_get_writing'},
            {'trigger': 'advance', 'source':'init', 'dest':'edit_code', 'conditions':'is_going_to_edit_code'},
            {'trigger': 'advance', 'source':'edit_code', 'dest':'get_code', 'conditions':'is_going_to_get_code'},
            {'trigger': 'advance', 'source':'get_code', 'dest':'get_inst', 'conditions':'is_going_to_get_inst'},
            {'trigger': 'advance', 'source':'get_inst', 'dest':'get_code', 'conditions':'is_going_to_get_code'},
            {'trigger': 'advance', 'source':'init', 'dest':'generate_image', 'conditions':'is_going_to_generate_image'},
            {'trigger': 'advance', 'source':'generate_image', 'dest':'create_image', 'conditions':'is_going_to_create_image'},
            {'trigger': 'advance', 'source':'create_image', 'dest':'create_image', 'conditions':'is_going_to_create_image'},
            {'trigger': 'go_back',
            'source':[
            'user', 'init',
            'chat', 'conversation',
            'edit_text', 'get_writing',
            'edit_code', 'get_code', 'get_inst',
            'generate_image', 'create_image'
            ], 'dest':'init'}

        ],
        initial='user',
        auto_transitions=False,
        show_conditions=True,
    )
    return machine

app = Flask(__name__, static_url_path='')


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route('/callback', methods=['POST'])
def webhook_handler():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if event.source.user_id not in machines:
            machines[event.source.user_id]=create_machine()
        machine = machines[event.source.user_id]

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')    

        response = machine.advance(event)
        if response == False:
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, 'https://i.postimg.cc/pX4gx1NP/fsm.png')
            else:
                machine.go_back(event)

    return 'OK'

if __name__ == '__main__':
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port, debug=True)
