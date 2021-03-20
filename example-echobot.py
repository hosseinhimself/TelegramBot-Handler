import telegrambot

TelegramUpdate = telegrambot.TelegramUpdate(TOKEN) # define a telegram bot

commands = telegrambot.commands()  # you need this line to set commands
commands.addCommands(command="start", answer = "Welcome!") # add a new command, I added (/start) here

Status = True
while Status:
    message = TelegramUpdate.getUpdates()
    if message != None :
        if message.text in commands.commands:
            TelegramUpdate.sendMessage(text = commands.commands[message.text],chatid = message.chatid) #send commands massages
        else:
            TelegramUpdate.sendMessage(text = message.text , chatid = message.chatid) #sending echo to user