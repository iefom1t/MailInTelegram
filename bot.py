import json
import imaplib
import time
import telebot


with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

interval = config['Interval']
mailboxes = config['Mailboxes']
owner_id = config['OwnerID']
token = config['BotToken']

unseen = {}

logger = telebot.logging.getLogger()
telebot.logging.basicConfig(filename="logs/bot.log",
                            datefmt='%d-%m-%Y %H:%M:%S',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='w+',
                            encoding='utf-8',
                            level=telebot.logging.INFO)

bot = telebot.TeleBot(token, parse_mode='html')


def not_owner(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    bot.send_message(chat_id, 'You are not owner!')
    logger.info("Access denied to user %s", user_id)


def check_mail():
    summary = 0

    for mailbox in mailboxes:
        host, port, tls = mailbox['Host'], mailbox['Port'], mailbox['TLS']
        email, password = mailbox['Email'], mailbox['Password']

        if tls:
            conn = imaplib.IMAP4_SSL(host, port, timeout=5)
        else:
            conn = imaplib.IMAP4(host, port, timeout=5)

        try:
            resp_code, resp = conn.login(email, password)
            logger.info('%s is OK: %s - %s', email,
                        resp_code, resp[0].decode())
        except Exception as error:
            logger.error('%s is BAD: %s', email, error)
            continue

        try:
            conn.select(mailbox='INBOX', readonly=1)
            resp_code, resp = conn.search(None, 'UNSEEN')

            if resp_code == 'OK':
                messages = resp[0].decode()
                num_unseen = len(messages.split(' ')) if messages != '' else 0

            if email not in unseen:
                unseen[email] = num_unseen

            elif unseen[email] < num_unseen:
                diff = num_unseen - unseen[email]
                unseen[email] = num_unseen
                summary += diff
        except conn.abort as error:
            logger.error('%s is BAD: %s', email, error)
            continue

        conn.close()
        conn.logout()

    return summary


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id != owner_id:
        not_owner(message)
        return

    bot.send_message(chat_id, 'Hello!')
    bot.send_message(
        chat_id, f'Fetching mailboxes every {interval} seconds...')

    while True:
        msgs = check_mail()
        if msgs:
            bot.send_message(
                chat_id, f'<b>{msgs} message(s) arrived.</b>', parse_mode='HTML')

        time.sleep(interval)


if __name__ == '__main__':
        bot.infinity_polling()
