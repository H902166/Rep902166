import requests
import datetime

class BotHandler:
    def __init__(self, token):
        #self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=10):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp


    def get_last_update(self, null=None):
        get_result = self.get_updates()
        print("get_result=",get_result)
        print("length=",len(get_result))
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None#get_result[len(get_result)]
        return last_update

token = "1818877620:AAHV634YyAZPSHye8H6a_0xVvC4Yv11uzu0"

greet_bot = BotHandler(token)
greetings = ('hello', 'hi', 'greetings', 'sup')
now = datetime.datetime.now()

def main(null=None):
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()
        if last_update != None:

            print("last_update=",last_update)
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']
            print("last_chat_text=",last_chat_text)

            #if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            if last_chat_text.lower() in greetings:# and today == now.day and  hour < 12:
                greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))
                #today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
                greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
                greet_bot.send_message(last_chat_id, 'Good Evening  {}'.format(last_chat_name))
                today += 1

            new_offset = last_update_id + 1
            print(new_offset)
        else:
            print("None")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()