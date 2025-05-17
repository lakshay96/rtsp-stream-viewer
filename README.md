# rtsp-stream-viewer

A full-stack web application that allows users to add RTSP stream URLs and view the live streams in a browser using WebSockets.

---

## 🚀 Live Demo

- **Frontend**: [https://lakshay96.github.io/rtsp-stream-viewer](https://lakshay96.github.io/rtsp-stream-viewer)
- **Backend**: [https://rtsp-backend.herokuapp.com](https://rtsp-backend.herokuapp.com) 

---

## 📦 Tech Stack

### Frontend:
- React.js (CRA)
- Material UI (MUI)
- WebSocket client

### Backend:
- Django
- Django Channels (WebSockets)
- OpenCV + FFmpeg

---

## 📁 Project Structure

```
rtsp-stream-viewer/
├── backend/               # Django + Channels + FFmpeg backend
│   ├── streamer/          # ASGI setup and routing
│   ├── streams/           # WebSocket consumers and OpenCV stream logic
│   └── manage.py
├── frontend/              # React frontend with MUI
│   ├── src/               # React components
│   └── public/
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/lakshay96/rtsp-stream-viewer.git
cd rtsp-stream-viewer
```

---

### 2. Frontend (React)
```bash
cd frontend
npm install
npm start
```
Visit: `http://localhost:3000`

---

### 3. Backend (Django + Channels)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Visit: `http://localhost:8000`

To serve WebSocket via ASGI:
```bash
daphne streamer.asgi:application --port 8000 --bind 0.0.0.0
```

---

## 🌐 Deployment

### Frontend: GitHub Pages
```bash
npm run deploy
```
Make sure `package.json` has:
```json
"homepage": "https://lakshay96.github.io/rtsp-stream-viewer"
```

### Backend: Heroku
```bash
heroku login
heroku create rtsp-backend
heroku buildpacks:add heroku/python
heroku config:set DISABLE_COLLECTSTATIC=1

# Create Procfile in backend directory:
echo "web: daphne streamer.asgi:application --port \$PORT --bind 0.0.0.0" > Procfile

# Commit and push backend
cd backend
git init
git add .
git commit -m "Initial backend push"
git push heroku master
```

---

## 🧪 Testing RTSP Streams

Try any of the following RTSP URLs:
- `rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov`
- `rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov`

Paste into the input field on the React app and hit "Add Stream".

---

## ❓ FAQ

### What if my camera doesn't load?
- Make sure it's not blocked by the browser or system permissions.
- Try loading a public RTSP stream instead.

### Backend fails to open stream?
- Confirm `opencv-python` is installed.
- Ensure video file or RTSP source is valid.

---

## 👤 Author
**Lakshay Aggarwal**  
[GitHub: lakshay96](https://github.com/lakshay96)
