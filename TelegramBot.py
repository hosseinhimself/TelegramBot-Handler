import json
from urllib.request import urlopen
from urllib.parse import quote, unquote
import time

def aux_dec2utf8(resp):
    decoded = ''
    for line in resp:
        decoded += line.decode('utf-8')
    return decoded

class UpdateMessage:
    def __init__(self,text,chatid,replyid):
        self.text = text
        self.chatid = chatid
        self.reply_to_message_id = replyid

class commands:
    def __init__(self):
        self.commands={}
    def addCommands(self,command,answer):
        self.commands["/{}".format(command)] = answer



class TelegramUpdate:
    def __init__(self,token):
        self.token = token
        self.url   = 'https://api.telegram.org/bot{}/'.format(self.token)
        cmd   = 'getme'                                               
        resp  = urlopen(self.url + cmd)
        line  = aux_dec2utf8(resp)
        gtm   = json.loads(line)

    def getUpdates(self):
        cmd = 'getUpdates'
        try:
            resp = urlopen(self.url + cmd)
            line = aux_dec2utf8(resp)
            upds = json.loads(line)
            NoM  = len(upds['result'])
            if NoM != 0:
                if 'edited_message' in upds:
                    return None
                msg  = upds['result'][0]['message']
                chid = str(msg['chat']['id'])

                if 'reply_to_message' in msg:
                    replyid =str(msg['reply_to_message']['message_id'])
                    
                else:
                    replyid = None
                print("inja",replyid)
                if 'text' in msg:
                    txt  = msg['text']
                    message = UpdateMessage(txt,chid,replyid)
                    uid = upds['result'][0]['update_id']               # Read the update id
                    cmd = 'getUpdates'                                 # Auxilary variable for defining commands
                    urlopen(self.url + cmd + '?offset={}'.format(uid + 1))
                    return message
                else:
                    uid = upds['result'][0]['update_id']                   # Read the update id
                    cmd = 'getUpdates'                                     # Auxilary variable for defining commands
                    urlopen(self.url + cmd + '?offset={}'.format(uid + 1))
        except:
            print("Error")

        time.sleep(5)
        

    def sendMessage(self,text , chatid , reply_to_message=None):
        cmd  = 'sendMessage'
        txt = quote(text.encode('utf-8'))
        link = self.url + cmd + '?chat_id={}&text={}'.format(chatid, txt)
        if reply_to_message != None:
            link = link + '&reply_to_message_id={}'.format(reply_to_message)
        resp = urlopen(link) 
        line = aux_dec2utf8(resp)                              # converting the content to utf-8
        chck = json.loads(line)                                # converting the content to JSON
        if chck['ok']:                                         # If sending was successfull
            uid = upds['result'][0]['update_id']               # Read the update id
            cmd = 'getUpdates'                                 # Auxilary variable for defining commands
            urlopen(self.url + cmd + '?offset={}'.format(uid + 1))
        time.sleep(5)

    def findMessageText(self,message_id):
        cmd = 'getUpdates'
        resp = urlopen(self.url + cmd)
        line = aux_dec2utf8(resp)
        upds = json.loads(line)
        NoM  = len(upds['result'])
        msg = upds['result']
        if NoM != 0:
            for i in msg:
                if "message" in i and i["message"]["message_id"] == message_id:
                    return i["message"]["text"]


        
