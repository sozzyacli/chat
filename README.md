# Simple 2-Person Chat App

A lightweight Flask + SocketIO chat application designed for easy deployment on PythonAnywhere.

## Features
- Real-time messaging with WebSockets
- User login with session management
- Online user list
- Clean, responsive UI
- Works on PythonAnywhere free tier

## Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Visit `http://localhost:5000` - open in two browser tabs to test.

---

## PythonAnywhere Deployment (Free Tier)

### 1. Upload Files
- Go to **Files** tab in PythonAnywhere dashboard
- Create folder `chat_app` in your home directory
- Upload all files maintaining this structure:
  ```
  /home/yourusername/chat_app/
  ├── app.py
  ├── requirements.txt
  └── templates/
      ├── login.html
      └── chat.html
  ```

### 2. Create Virtual Environment
```bash
# In a Bash console on PythonAnywhere
cd ~/chat_app
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Web App
1. Go to **Web** tab → **Add a new web app**
2. Choose **Manual configuration** → **Python 3.10**
3. Set **Source code**: `/home/yourusername/chat_app`
4. Set **Working directory**: `/home/yourusername/chat_app`

### 4. Edit WSGI File
Click the WSGI configuration file link and replace with:

```python
import sys
import os

# Add your project directory
path = '/home/yourusername/chat_app'
if path not in sys.path:
    sys.path.insert(0, path)

# Activate virtual environment
activate_this = '/home/yourusername/chat_app/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

from app import app as application

# For SocketIO support on PythonAnywhere
# Note: Free tier only supports HTTP, not WebSockets
# For WebSockets, you need a paid plan or use a different host
```

### 5. Set Environment Variable
In **Web** tab → **Environment variables**, add:
- `SECRET_KEY` = `your-random-secret-key-here`

### 6. Reload Web App
Click **Reload** button on the Web tab.

### 7. Access Your Chat
Visit `https://yourusername.pythonanywhere.com`

---

## ⚠️ PythonAnywhere Free Tier Limitation

**The free tier does NOT support WebSockets.** SocketIO will fall back to long-polling which works but isn't real-time.

### Options for Real WebSockets:
1. **Upgrade to Hacker plan ($5/mo)** - enables WebSocket support
2. **Use a different host** with free WebSockets:
   - **Render.com** (free tier with WebSockets)
   - **Railway.app** (free tier)
   - **Fly.io** (free allowance)
   - **Heroku** (no longer free)

---

## Render.com Deployment (Free with WebSockets)

1. Push this repo to GitHub
2. On Render: **New → Web Service** → Connect GitHub repo
3. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -k eventlet -w 1 app:app`
   - **Environment**: Add `SECRET_KEY` and `PORT=10000`
4. Deploy - you'll get a `https://your-app.onrender.com` with real WebSockets!

---

## Project Structure
```
chat_app/
├── app.py              # Main Flask + SocketIO app
├── requirements.txt    # Python dependencies
└── templates/
    ├── login.html      # Login page
    └── chat.html       # Chat interface
```

## Customization
- Change `SECRET_KEY` in production (use `python -c "import secrets; print(secrets.token_hex(32))"`)
- Modify max username length in `app.py` and `login.html`
- Adjust styling in the `<style>` blocks in templates
- Add features: private messages, rooms, message persistence, etc.

## License
MIT - Feel free to use and modify.