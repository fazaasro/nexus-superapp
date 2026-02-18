# Nexus Web UI - Quick Start Guide

## 🚀 Start the Application

### Option 1: Quick Start Script
```bash
cd /home/ai-dev/.openclaw/workspace
./start.sh
```

### Option 2: Manual Start

**Backend (Terminal 1):**
```bash
cd /home/ai-dev/.openclaw/workspace
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend (Terminal 2):**
```bash
cd /home/ai-dev/.openclaw/workspace/web-ui
npm run dev
```

### Option 3: Docker
```bash
cd /home/ai-dev/.openclaw/workspace
docker-compose up -d
```

## 📱 Access the App

Once started, open your browser to:
```
http://localhost:5173
```

API documentation available at:
```
http://localhost:8000/docs
```

## ✨ Features

- **Mobile-First Design** - Works beautifully on phone, tablet, and desktop
- **Dark Mode** - Automatic detection + manual toggle
- **Real-Time Updates** - Live data across all modules
- **Unified Dashboard** - One app for Finance, Knowledge, Social, and Health

## 📊 Modules

1. **💰 Finance (The Bag)** - Track spending, receipts, budget
2. **🧠 Knowledge (The Brain)** - Capture learning, Anki integration
3. **👥 Social (The Circle)** - Contacts, health logs, mood
4. **❤️ Health (The Vessel)** - Blueprint protocol, workouts, biometrics

## 🐛 Troubleshooting

**Port 8000 in use?**
```bash
lsof -i :8000
kill -9 <PID>
```

**Port 5173 in use?**
```bash
lsof -i :5173
kill -9 <PID>
```

**Install dependencies:**
```bash
cd web-ui && npm install
```

## 📚 Documentation

- Full Setup Guide: `WEB_UI_SETUP.md`
- Implementation Summary: `WEB_UI_IMPLEMENTATION_SUMMARY.md`
- Subagent Log: `SUBAGENT_LOG.md`
- Web UI README: `web-ui/README.md`

---

Built with ❤️ using Vue 3 + FastAPI
