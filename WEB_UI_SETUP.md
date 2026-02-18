# Nexus Super App - Web UI Setup Guide

This guide will help you set up and run the Nexus Super App web interface.

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **Docker** (optional, for containerized deployment)

## 🚀 Quick Start

### Option 1: Using the Setup Script

```bash
# Run the setup script
./start.sh
```

This will:
1. Check for required dependencies
2. Install Python dependencies
3. Install Node.js dependencies
4. Create necessary directories

### Option 2: Manual Setup

#### Step 1: Install Python Dependencies

```bash
# From workspace root
pip install -r requirements.txt
```

#### Step 2: Install Node Dependencies

```bash
cd web-ui
npm install
cd ..
```

#### Step 3: Create Data Directory

```bash
mkdir -p data
```

## 🏃 Running the Application

### Development Mode

#### Terminal 1: Start Backend API

```bash
# From workspace root
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

#### Terminal 2: Start Frontend

```bash
cd web-ui
npm run dev
```

The frontend will be available at:
- Frontend: http://localhost:5173

#### Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

### Production Mode (Docker)

#### Build and Start

```bash
# From workspace root
docker-compose up -d
```

This will:
1. Build the backend Docker image
2. Build the frontend Docker image
3. Start both services
4. Configure nginx to serve the frontend
5. Set up API proxy

#### Access the Application

```
Frontend: http://localhost:5173
API:      http://localhost:8000
API Docs: http://localhost:8000/docs
```

#### View Logs

```bash
# View all logs
docker-compose logs -f

# View only API logs
docker-compose logs -f nexus-api

# View only web logs
docker-compose logs -f nexus-web
```

#### Stop Services

```bash
docker-compose down
```

#### Rebuild After Changes

```bash
# Rebuild and restart
docker-compose up -d --build

# Or rebuild specific service
docker-compose up -d --build nexus-api
```

## 📁 Project Structure

```
workspace/
├── api/                    # Backend API
│   └── main.py            # FastAPI application
├── modules/               # Module implementations
│   ├── bag/               # Finance module
│   ├── brain/             # Knowledge module
│   ├── circle/            # Social module
│   └── vessel/            # Health module
├── web-ui/                # Frontend application
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # Reusable components
│   │   ├── plugins/      # Vue plugins
│   │   ├── router/       # Routing
│   │   ├── stores/       # State management
│   │   └── views/        # Page components
│   ├── package.json      # Node dependencies
│   ├── vite.config.js    # Vite configuration
│   └── Dockerfile        # Docker configuration
├── data/                  # SQLite database and data files
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker orchestration
└── start.sh              # Quick start script
```

## 🔧 Configuration

### API Proxy (Development)

The frontend proxies API requests to the backend in development:

```javascript
// web-ui/vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true
    }
  }
}
```

### Environment Variables

Create `.env` files as needed:

#### Backend (.env)
```
DATABASE_URL=sqlite:///./data/nexus.db
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
```

#### Frontend (web-ui/.env)
```
VITE_API_URL=http://localhost:8000/api/v1
```

## 📱 Features

### Mobile-First Design
- Responsive layout (mobile, tablet, desktop)
- Bottom navigation for mobile
- Sidebar for desktop
- Touch-optimized interface

### Dark Mode
- Automatic detection of system preference
- Manual toggle in sidebar
- Persists user preference

### Real-Time Updates
- Reactive state with Pinia
- Live data across all modules
- Optimistic UI updates

### Unified Dashboard
- Single app for all 4 modules
- Quick navigation
- Cross-module insights

## 🔐 Authentication

The application currently uses test authentication. For production:

1. Implement proper JWT authentication in the backend
2. Update the API client to include tokens
3. Configure Cloudflare Access for your domain

## 🌐 Deployment

### Cloudflare Tunnel (Recommended)

1. Start the application with Docker:
   ```bash
   docker-compose up -d
   ```

2. Configure Cloudflare Tunnel to route:
   - `nexus.yourdomain.com` → `localhost:5173`
   - `nexus-api.yourdomain.com` → `localhost:8000`

3. Access via your domain:
   - Frontend: `https://nexus.yourdomain.com`
   - API: `https://nexus-api.yourdomain.com`

### Direct Deployment

1. Build the frontend:
   ```bash
   cd web-ui
   npm run build
   ```

2. Build Docker images:
   ```bash
   docker build -f Dockerfile.api -t nexus-api .
   docker build -f web-ui/Dockerfile -t nexus-web ./web-ui
   ```

3. Deploy to your preferred platform:
   - DigitalOcean
   - AWS ECS
   - Google Cloud Run
   - Heroku
   - Your VPS

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=modules --cov=api --cov-report=html
```

### Frontend Tests

```bash
cd web-ui

# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e
```

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process
lsof -i :8000
kill -9 <PID>
```

**Database errors:**
```bash
# Recreate the database
rm data/nexus.db
# The app will recreate it on startup
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Kill the process
lsof -i :5173
kill -9 <PID>
```

**Module not found:**
```bash
cd web-ui
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
# Clear cache and rebuild
cd web-ui
npm run build -- --force
```

### Docker Issues

**Containers won't start:**
```bash
# Check logs
docker-compose logs

# Rebuild images
docker-compose up -d --build

# Remove everything and start fresh
docker-compose down -v
docker-compose up -d --build
```

## 📊 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🎨 Customization

### Theming

Edit the Vuetify theme in `web-ui/src/plugins/vuetify.js`:

```javascript
theme: {
  themes: {
    light: {
      colors: {
        primary: '#6366f1',  // Change this
        // ... other colors
      }
    }
  }
}
```

### Module Configuration

Each module has its own configuration:

- **Finance:** Edit bag settings in `modules/bag/`
- **Knowledge:** Edit brain settings in `modules/brain/`
- **Social:** Edit circle settings in `modules/circle/`
- **Health:** Edit vessel settings in `modules/vessel/`

## 🚀 Performance Optimization

### Frontend

- Enable compression in nginx
- Use CDN for static assets
- Implement lazy loading for images
- Use code splitting for routes

### Backend

- Add Redis caching
- Implement database connection pooling
- Use async database operations
- Add rate limiting

## 📝 Development Workflow

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```

2. Make your changes

3. Test thoroughly:
   ```bash
   npm run test
   pytest
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

5. Push and create a PR

## 🤝 Contributing

1. Follow the code style guide
2. Write tests for new features
3. Update documentation
4. Test on multiple screen sizes
5. Ensure all tests pass

## 📚 Additional Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Vuetify Documentation](https://vuetifyjs.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)

## 🆘 Support

For issues and questions:
1. Check this documentation
2. Review the API docs at `/docs`
3. Check existing GitHub issues
4. Create a new issue if needed

---

Built with ❤️ using Vue 3 + FastAPI
