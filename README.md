<img width="1280" height="640" alt="изображение" src="https://github.com/user-attachments/assets/366f9beb-bddb-42fc-8551-aa310a59d9aa" />

# get2id

Get any Telegram ID in one tap. Send or forward a message and the bot shows the IDs and file data hidden inside it. Fast and stable, built with [aiogram](https://github.com/aiogram/aiogram) 3.

## Features

- **User info**: ID, name, username, bot and premium flags, language, estimated account creation date.
- **Forwarded messages**: shows who the message came from (user, chat or channel) with their IDs. For users who hide forwarding, only the name is available.
- **Files and media**: `file_id`, `file_unique_id`, size, type-specific details and caption for:
  stickers, photos, documents, audio, voice messages, videos, video notes (circles), GIFs.
- **Contacts and locations**: phone, user ID (if the contact has Telegram), coordinates with a map link.
- **Text and custom emoji**: message info plus the ID of every custom (premium) emoji in the text, ready to copy.
- **Tap to copy**: IDs and file IDs are wrapped in monospace, so one tap copies them.

## Commands

| Command  | Description                  |
| -------- | ---------------------------- |
| `/start` | Greeting and your own ID     |
| `/info`  | Information about your account |
| `/dev`   | Developer contacts           |

## Creation date

Telegram does not share the real registration date of an account. The bot estimates it from the user ID, because IDs are issued roughly in order. The result is approximate and can be off by several months. For the newest accounts only a "newer than" date is shown. A button under the answer explains this to the user.

## Installation

Requirements: Python 3.12+ and a bot token from [@BotFather](https://t.me/BotFather).

```bash
git clone <your-repo-url>
cd get2id
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt`:

```
aiogram>=3.13
getids
```

## Configuration

Set your token as an environment variable (or in a `.env` file, never commit it):

```
BOT_TOKEN=123456:your-token-here
```

## Run

```bash
python main.py
```

For a server, run it under `systemd` or Docker so it restarts on failure. Only warnings and errors are written to the log.

## Project structure

```
.
├── main.py            # bot startup, polling
├── handlers.py        # all message handlers and helpers
├── requirements.txt
└── README.md
```

## Notes

- Custom emoji (`<tg-emoji>`) are shown only if the bot is allowed to send them. Otherwise Telegram falls back to the regular emoji, so the messages stay readable.
- Bots can download files up to 20 MB through the Bot API.
- Handlers are matched in order: `F.animation` must be above `F.document`, and `F.text` must be the last handler.

## Developer

[@pheophore](https://t.me/pheophore)
