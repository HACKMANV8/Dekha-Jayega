# Quick Start Guide - Dekha-Jayega Multi-Agent Integration

## Prerequisites Checklist

- [ ] Node.js installed
- [ ] Python 3.8+ installed
- [ ] MongoDB running (local or Atlas)
- [ ] API Keys ready (Google Gemini and/or OpenAI)

## Step-by-Step Startup

### 1. Configure Environment Variables

#### Backend `.env` (d:\Dekha-Jayega\Backend\.env)

```env
MONGODB_URI=your_mongodb_connection_string_here
SAGA_API_URL=http://localhost:8001
GEMINI_API_KEY=your_gemini_api_key_here
PORT=4000
```

#### Python Saga API `.env` (d:\Dekha-Jayega\Hackman_agent-main\.env)

```env
GOOGLE_API_KEY=your_google_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
# Optional:
SUPERVISOR_MODEL=gemini-2.0-flash-exp
API_PORT=8001
```

#### Nano Banana Python `.env` (d:\Dekha-Jayega\Nano banana\nano-banana-python\.env)

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Install Dependencies (First Time Only)

#### Backend

```powershell
cd "d:\Dekha-Jayega\Backend"
npm install
```

#### Frontend

```powershell
cd "d:\Dekha-Jayega\Frontend"
npm install
```

#### Python Saga API

```powershell
cd "d:\Dekha-Jayega\Hackman_agent-main"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start All Servers

Open **THREE** separate PowerShell terminals:

#### Terminal 1: Python Saga API Server

```powershell
cd "d:\Dekha-Jayega\Hackman_agent-main"
venv\Scripts\activate
python saga_api_server.py
```

**Wait for**: `Uvicorn running on http://0.0.0.0:8001`

#### Terminal 2: Node.js Backend

```powershell
cd "d:\Dekha-Jayega\Backend"
npm run dev
```

**Wait for**: `🚀 Project X API Server is running on port 4000`

#### Terminal 3: React Frontend

```powershell
cd "d:\Dekha-Jayega\Frontend"
npm run dev
```

**Wait for**: `Local: http://localhost:5173/`

### 4. Access the Application

1. **Frontend**: http://localhost:5173/agents
2. **Backend API**: http://localhost:4000/api/health
3. **Python API Docs**: http://localhost:8001/docs

### 5. Test the Integration

1. Navigate to: http://localhost:5173/agents
2. Enter a topic: "A steampunk detective RPG in Victorian London"
3. Click "Start Saga Generation"
4. Wait 30-60 seconds for generation
5. Check browser console for session ID
6. Verify success message appears

### Quick Health Check Commands

```powershell
# Check Backend
curl http://localhost:4000/api/health

# Check Python API
curl http://localhost:8001/docs

# Check Frontend (open in browser)
# http://localhost:5173
```

### Troubleshooting

#### Python Server Won't Start

```powershell
# Check if port 8001 is in use
netstat -ano | findstr :8001

# Kill the process if needed
taskkill /PID <PID> /F

# Verify API keys in .env
cd "d:\Dekha-Jayega\Hackman_agent-main"
type .env
```

#### Backend Can't Connect to MongoDB

```powershell
# Test MongoDB connection
cd "d:\Dekha-Jayega\Backend"
node -e "require('mongoose').connect(process.env.MONGODB_URI).then(() => console.log('✅ Connected')).catch(err => console.error('❌', err))"
```

#### Backend Can't Reach Python API

```powershell
# Test Python API from Backend directory
curl http://localhost:8001/docs

# Check SAGA_API_URL in Backend/.env
cd "d:\Dekha-Jayega\Backend"
type .env | findstr SAGA_API_URL
```

#### Frontend Errors

```powershell
# Clear cache and reinstall
cd "d:\Dekha-Jayega\Frontend"
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json
npm install
npm run dev
```

### Stopping All Servers

Press `Ctrl+C` in each terminal window, or:

```powershell
# Stop all Node.js processes
taskkill /F /IM node.exe

# Stop all Python processes
taskkill /F /IM python.exe
```

### Next Steps After Successful Test

1. Review `INTEGRATION_GUIDE.md` for detailed API documentation
2. Review `COMPLETE_SUMMARY.md` for feature status
3. Test the full workflow:
   - Create project
   - Start saga generation
   - Check MongoDB for stored data
   - Test image generation
4. Enhance `Frontend/src/pages/Agents.jsx` with full wizard UI (see guides)

### Important URLs

- **Frontend**: http://localhost:5173
- **Agents Page**: http://localhost:5173/agents
- **Dashboard**: http://localhost:5173/dashboard
- **Backend API Health**: http://localhost:4000/api/health
- **Python API Docs**: http://localhost:8001/docs
- **Python API Swagger**: http://localhost:8001/redoc

### File Structure Reference

```
d:\Dekha-Jayega\
├── Backend\
│   ├── .env (create this)
│   ├── src\
│   │   ├── controller\
│   │   │   ├── sagaAgentController.js ✅ NEW
│   │   │   └── sagaImageController.js ✅ NEW
│   │   ├── model\
│   │   │   └── SagaSession.js ✅ NEW
│   │   └── routes\
│   │       └── sagaAgentRoutes.js ✅ NEW
│   └── package.json (updated)
├── Frontend\
│   └── src\
│       └── pages\
│           └── Agents.jsx (updated)
├── Hackman_agent-main\
│   ├── .env (create this)
│   ├── saga_api_server.py
│   └── venv\ (create this)
├── Nano banana\
│   └── nano-banana-python\
│       └── .env (create this)
├── INTEGRATION_GUIDE.md ✅
├── COMPLETE_SUMMARY.md ✅
└── QUICK_START.md (this file) ✅
```

### Success Indicators

You've successfully integrated everything when:

- ✅ All three servers start without errors
- ✅ Frontend loads at localhost:5173
- ✅ Topic input triggers saga generation
- ✅ Browser console shows session ID
- ✅ MongoDB contains new saga session document
- ✅ No errors in any terminal window

### Getting Help

1. Check logs in each terminal for error messages
2. Review `INTEGRATION_GUIDE.md` for troubleshooting
3. Verify all API keys are correct
4. Ensure all dependencies are installed
5. Check MongoDB connection string

---

**Ready to start? Open three terminals and follow Step 3!** 🚀
