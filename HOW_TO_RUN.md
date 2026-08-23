# How to run this thing

So you cloned the repo and now you're staring at a folder of Python files. Here's how to get it actually running on your machine. Should take about five minutes, most of which is waiting on `pip`.

## What you need first

- **Python 3.11 or newer.** Check with `python3 --version`. If that errors out, grab it from [python.org](https://www.python.org/downloads/).
- A terminal. Whatever you've got.

That's it. No database to install, no Docker, nothing else.

## Getting it running

**1. Grab the code and go into the folder**

```bash
git clone https://github.com/Anant-Madhok231/InsiderInfo.git
cd InsiderInfo
```

**2. Make a virtual environment**

This keeps the project's packages separate from the rest of your system, so you don't end up with twelve versions of Flask fighting each other.

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows that last line is `venv\Scripts\activate` instead.

You'll know it worked because your prompt now has `(venv)` stuck on the front.

**3. Install everything**

```bash
pip install -r requirements.txt
```

This one takes a minute. `yfinance` pulls in pandas, which is chunky.

**4. Set up your keys**

The app needs a few API keys and an email login to do its thing. None of them are in the repo — you supply your own.

```bash
cp .env.example .env
```

Now open `.env` in whatever editor you like and fill in the blanks. Here's what each one is and where to get it:

| Variable | What it's for | Where to get it |
|---|---|---|
| `MAIL_USERNAME` | The Gmail address that sends signup codes | Your own Gmail |
| `MAIL_PASSWORD` | An app password, **not** your actual Gmail password | [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |
| `SECRET_KEY` | Signs login cookies so people can't forge them | Generate one, see below |
| `ALPHA_VANTAGE_API_KEY` | Stock quotes | [Free key here](https://www.alphavantage.co/support/#api-key) |
| `FMP_API_KEY` | More market data | [Free key here](https://site.financialmodelingprep.com/developer/docs) |
| `POLYGON_API_KEY` | Also market data | [polygon.io](https://polygon.io/dashboard/api-keys) |

For `SECRET_KEY`, just run this and paste the output:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**A note on the Gmail one:** app passwords only show up as an option if you have 2-factor auth turned on for that Google account. If you don't see the page, that's why. And use a throwaway Gmail for this, not your main one.

**5. Run it**

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) and you're in.

To stop it, hit `Ctrl+C` in the terminal.

## What if I skip the keys?

It'll still start. You'll get warnings in the terminal like `[config] FMP_API_KEY is not set` and the parts that need that key just won't work — the ticker will be empty, signup emails won't send. Nothing crashes, you just get a hollow version of the site. Fine if you only want to poke around the UI.

## Things that go wrong

**`ModuleNotFoundError: No module named 'flask'`**

Your virtual environment isn't active. Run `source venv/bin/activate` again — you have to do this every time you open a new terminal.

**The homepage loads but the stock ticker is empty**

Either your Alpha Vantage key is missing, or you hit the rate limit. The free tier is 5 calls a minute and 25 a day, which is not a lot. Wait a bit and reload.

**Signup says "Error sending verification email"**

Nine times out of ten this is the Gmail app password. Make sure you used an *app password* from the link above and not your regular account password — Google blocks regular passwords for SMTP. Also check there aren't stray spaces when you pasted it.

**Port 5000 is already in use**

Something else has it. On a Mac it's usually AirPlay Receiver — turn it off in System Settings, or just run on a different port:

```bash
PORT=5001 python app.py
```

**The options search returns nothing**

The app downloads a big options CSV from Google Drive the first time you search. If your network blocked it or it timed out, you'll get empty results. Check the terminal — it prints the download progress and any error.

## Where stuff lives

```
app.py             # all the routes and page logic
config.py          # reads your .env, no secrets in here
models.py          # the User table
templates/         # the HTML pages
static/            # CSS and JS
.env               # your keys (never commit this)
```

Accounts get saved to a small SQLite file that gets created automatically on first run. It's gitignored, so it stays on your machine.

## Putting it online

There's a `render.yaml` and a `Procfile` in here already, so [Render](https://render.com) works out of the box on the free tier. Point it at this repo, then add all those same variables from your `.env` under the service's **Environment** tab. Don't put them in the code.

Fair warning: Render's free tier puts your app to sleep after 15 minutes of nobody visiting, so the first load after a quiet spell takes 30-60 seconds to wake up. Totally normal, not broken.
