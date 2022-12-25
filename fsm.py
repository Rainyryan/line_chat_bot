from transitions.extensions import GraphMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
from bs4 import BeautifulSoup
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
import pandas as pd

from openai_api import chat, edit_text, edit_code, generate_image


# global variable
prompt = ''
inst = ''

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start

    def is_going_to_init(self, event):
        return True
    
    def on_enter_init(self, event):
        title = 'Aaaaaaahhhhhhh 0.0'
        text = "You woke the Totoro up, what to do next?"
        btn = [
            MessageTemplateAction(
                label = 'chat with me!',
                text ='chat'
            ),
            MessageTemplateAction(
                label = 'fix my writing',
                text = 'edit_text'
            ),
            MessageTemplateAction(
                label = 'fix my code',
                text = 'edit_code'
            ),
            MessageTemplateAction(
                label = 'make cool images',
                text = 'generate_image'
            ),            
        ]
        url = 'https://www.japansociety.org/wp-content/uploads/elementor/thumbs/Totoro_-_1920x1080-ptmuy8sfp2m84s2lq9q9k9xzfdqjz9es3zvtkwesz4-1-1-px1ayqnheb7eaw6ed8ujgsbwduc6t9qnr4mm83e9f4.webp'
        send_button_message(event.reply_token, title, text, btn, url)
    
    def is_going_to_chat(self, event):
        return event.message.text == 'chat'
    def on_enter_chat(self, event):
        send_text_message(event.reply_token, chat("have a chat with me"))

    def is_going_in_conversation(self, event):
        return event.message.text.lower() != 'back'
    def on_enter_conversation(self, event):
        send_text_message(event.reply_token, chat(event.message.text))

        
    def is_going_to_edit_text(self, event):
        return event.message.text == 'edit_text'
    
    def on_enter_edit_text(self, event):
        send_text_message(event.reply_token, "Enter your writing")

    def is_going_to_get_writing(self, event):
        return event.message.text.lower() != 'back'
    def on_enter_get_writing(self, event):
        send_text_message(event.reply_token, edit_text(event.message.text, "fix this piece of writing")+"\n\nYou can enter more writing, or enter 'back' to go back.")

    def is_going_to_edit_code(self, event):
        return event.message.text == 'edit_code'
    def on_enter_edit_code(self, event):
        send_text_message(event.reply_token, "Enter your code")

    def is_going_to_get_code(self, event):
        return event.message.text.lower() != 'back'
    def on_enter_get_code(self,event):
        global prompt
        prompt= event.message.text
        send_text_message(event.reply_token, "What do you want to do with your code?")


    def is_going_to_get_inst(self, event):
        return event.message.text.lower() != 'back'
    def on_enter_get_inst(self, event):
        send_text_message(event.reply_token, edit_code(prompt, event.message.text)+"\n\nYou can enter more code, or enter 'back' to go back.")


    def is_going_to_generate_image(self, event):
        return event.message.text == 'generate_image' or (self.state == 'create_image' and event.message.text.lower() != 'back')
    
    def on_enter_generate_image(self, event):
        send_text_message(event.reply_token, "What kind of an image do you want?")

    def is_going_to_create_image(self, event):
        return event.message.text.lower() != 'back'
    def on_enter_create_image(self, event):
        send_image_message(event.reply_token, generate_image(event.message.text))




