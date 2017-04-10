#!/usr/bin/env python3

import getpass
import logging
import logging.handlers
import os
import OpenReports

import chatexchange.client
import chatexchange.events

hostID = 'stackoverflow.com'
roomID = '111347'
selfID = 7829893

commands = {'o':'normal', 'open':'normal', 'ir':'ignore_rest', 'ignore rest':'ignore_rest',
        'fa':'fetch_amount', 'fetch amount':'fetch_amount'}

def _parseMessage(msg):
    temp = msg.split()
    return ' '.join(v for v in temp if not v[0] == '@')

def onMessage(message, client):
    try:
        if message.target_user_id != selfID:
            return
        userID = message.user.id
        command = _parseMessage(message.content)
        mode = commands[command]
    except:
        return
    
    message.message.reply(OpenReports.OpenReports(mode, userID=userID)) 


if 'ChatExchangeU' in os.environ:
    email = os.environ['ChatExchangeU']
else:
    email = input("Email: ")
if 'ChatExchangeP' in os.environ:
    password = os.environ['ChatExchangeP']
else:
    password = getpass.getpass("Password: ")

client = chatexchange.client.Client(hostID)
client.login(email, password)
print('Logged in')

room = client.get_room(roomID)
room.join()
print('Joined room')

watcher = room.watch(onMessage)
watcher.thread.join()


client.logout()

