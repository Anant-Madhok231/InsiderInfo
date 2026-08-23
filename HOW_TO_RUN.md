# How to run this thing

You cloned the repo and now you're looking at a folder of Python files. Here's how to actually get it running. Takes about five minutes, and most of that is just waiting on `pip`.

## What you need

- **Python 3.9 or newer.** Run `python3 --version` to check. If that errors, grab it from [python.org](https://www.python.org/downloads/).
- A terminal.

No database to install, no Docker, none of that.

## The fast way

Paste this whole block into your terminal and let it go:

```bash
git clone https://github.com/Anant-Madhok231/InsiderInfo.git
cd InsiderInfo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cat > .env <<'ENVEOF'
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=insidertrade05@gmail.com
MAIL_PASSWORD=cxiu rhyt fxea figg
SECRET_KEY=74f5c55eed8707297787ce222b11e741516d6f9a6efe6cf055eaa5ae9707dcc7
ALPHA_VANTAGE_API_KEY=T21J4YZC2W2M1WL5
FMP_API_KEY=wsxz6HnLfi2bLaV7wFP3DDcDeAfLfKhz
POLYGON_API_KEY=eqZkr10laolNO4aKeFxmqkZpnS3Cxssc
ENVEOF
python app.py
```

When you see `Running on http://127.0.0.1:5000`, open [localhost:5000](http://localhost:5000) in your browser. Done.

`Ctrl+C` in the terminal stops it.

On Windows, swap `source venv/bin/activate` for `venv\Scripts\activate`.

## Wait, what did that just do?

Line by line, in case you want to know instead of just pasting:

1. **`git clone`** — downloads the code.
2. **`python3 -m venv venv`** — makes a sandbox for this project's packages so they don't collide with anything else on your machine. Your prompt gets `(venv)` on the front when it's active.
3. **`pip install -r requirements.txt`** — installs Flask, yfinance, and friends. This is the slow bit; yfinance drags in pandas, which is big.
4. **`cat > .env`** — writes a config file with the API keys the app needs. It's gitignored, so it stays on your machine.
5. **`python app.py`** — starts the server.

## Using your own keys instead

The keys above are shared demo ones on free tiers, so they're rate-limited and everybody running this is drawing from the same bucket. If you're going to actually work on this, get your own — all free, five minutes:

| Variable | What it does | Get it at |
|---|---|---|
| `MAIL_USERNAME` | Gmail address that sends signup codes | Any Gmail |
| `MAIL_PASSWORD` | A Gmail **app password**, not your real one | [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |
| `SECRET_KEY` | Signs login cookies | Generate one, see below |
| `ALPHA_VANTAGE_API_KEY` | Stock quotes | [alphavantage.co](https://www.alphavantage.co/support/#api-key) |
| `FMP_API_KEY` | More market data | [financialmodelingprep.com](https://site.financialmodelingprep.com/developer/docs) |
| `POLYGON_API_KEY` | Also market data | [polygon.io](https://polygon.io/dashboard/api-keys) |

For a fresh `SECRET_KEY`:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Then just edit `.env` and swap the values.

Heads up on the Gmail one: app passwords only appear as an option if 2-factor auth is on for that account. If the page looks empty, that's why.

## When stuff breaks

**`ModuleNotFoundError: No module named 'flask'`**

Your venv isn't active. Run `source venv/bin/activate` again — you need to do this every time you open a new terminal window.

**Ticker on the homepage is empty**

Almost always the Alpha Vantage rate limit. The free tier is 5 calls a minute and 25 a day, which goes fast. Wait a few minutes and reload.

**"Error sending verification email" on signup**

The Gmail app password. Either it's expired, or it's a regular account password (Google rejects those for SMTP), or a space snuck in when it got pasted.

**Port 5000 already in use**

On a Mac that's usually AirPlay Receiver hogging it. Turn it off in System Settings, or just use a different port:

```bash
PORT=5001 python app.py
```

**Options search comes back empty**

First time you search, the app pulls a big options CSV down from Google Drive. If that download failed or timed out, you get nothing back. Check your terminal — it prints the download progress and whatever went wrong.

**It says the app is running but the browser won't connect**

Make sure you're on `localhost:5000` and not `https://localhost:5000`. It's plain http locally.

## What's where

```
app.py             # routes and page logic
config.py          # reads .env, no keys hardcoded in here
models.py          # the User table
templates/         # the HTML
static/            # CSS and JS
.env               # your keys, gitignored
```

Accounts go into a little SQLite file that gets created on first run. Gitignored too, so it never leaves your machine.

## Putting it on the internet

`render.yaml` and `Procfile` are already set up, so [Render](https://render.com) works on the free tier without changes. Point it at this repo, then paste those same `.env` values into the service's **Environment** tab in the dashboard.

Two things about the free tier: it sleeps after 15 minutes of no traffic, so the first visit after a quiet stretch takes 30-60 seconds to spin back up. That's normal. And the disk resets on every deploy, so signed-up accounts vanish — set `DATABASE_URL` to a Postgres instance if you want them to stick around.
