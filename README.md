# Mail in Telegram Bot

Bot that sends you notifications in Telegram about new mail in your mailboxes.

## Setup

```bash
git clone https://github.com/iefom1t/MailInTelegram
cd MailInTelegram
mkdir logs && touch logs/bot.log
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python generate_config.py
```

In this step, you should provide a bot token received from ```@BotFather```, your Telegram ID, interval between fetches
and information about your mailboxes. After you added all your mailboxes, type ```stop```.

Now you're ready to start bot:

```bash
python bot.py
```

Bot will fetch your mailboxes in a loop after ```/start``` command.

## License

Licensed under GNU General Public License v3.0.
