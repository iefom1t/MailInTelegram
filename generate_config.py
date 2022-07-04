import json

BotToken = input('Bot Token: ')
OwnerID = int(input('Owner ID: '))
interval = int(input('Fetch interval in seconds: '))

print('Now type your mailboxes data, use "stop" to stop :)')
mailboxes = []
inp = ''

while True:
    inp = input('Email Password Host Port TLS: ')
    if inp == 'stop':
        break

    email, password, host, port, tls = inp.split(' ')
    mailbox = {'Email': email, 'Password': password,
               'Host': host, 'Port': int(port), 'TLS': bool(tls)}

    mailboxes.append(mailbox)

config = {'BotToken': BotToken, 'OwnerID': OwnerID,
          'Interval': interval, 'Mailboxes': mailboxes}

with open('config.json', 'w', encoding='utf-8') as config_file:
    json.dump(config, config_file, ensure_ascii=False, indent=4)
