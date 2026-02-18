# Nexus Super App - Web UI

A modern, responsive web application unifying all 4 Nexus modules: Finance (The Bag), Knowledge (The Brain), Social (The Circle), and Health (The Vessel).

## 🚀 Features

### Mobile-First Design
- Responsive layout that works seamlessly on phone, tablet, and desktop
- Bottom navigation bar for mobile users
- Adaptive sidebar for desktop users
- Touch-optimized interface

### Dark Mode Support
- Automatic dark mode based on system preferences
- Manual theme toggle
- Persisted user preference

### Real-Time Data
- Live updates across all modules
- Reactive state management with Pinia
- Optimistic UI updates

### Unified Dashboard
- Single app for all 4 modules
- Quick navigation between modules
- Cross-module insights and stats

## 📦 Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and dev server
- **Vuetify 3** - Material Design component library
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - Database ORM
- **SQLite** - Embedded database

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and static file serving

## 🏗️ Project Structure

```
web-ui/
├── src/
│   ├── api/           # API client and endpoints
│   ├── components/    # Reusable components
│   ├── plugins/       # Vue plugins (Vuetify)
│   ├── router/        # Vue Router configuration
│   ├── stores/        # Pinia stores (state management)
│   ├── views/         # Page components
│   ├── App.vue        # Root component
│   └── main.js        # Entry point
├── public/            # Static assets
├── Dockerfile         # Docker build configuration
├── nginx.conf         # Nginx configuration
├── package.json       # Node dependencies
└── vite.config.js     # Vite configuration
```

## 🚦 Quick Start

### Development Mode

1. **Install dependencies:**
   ```bash
   cd web-ui
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Start backend API** (in another terminal):
   ```bash
   cd ..
   pip install -r requirements.txt
   uvicorn api.main:app --reload
   ```

4. **Open browser:**
   ```
   http://localhost:5173
   ```

### Production Mode (Docker)

1. **Build and start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   ```
   Frontend: http://localhost:5173
   API:      http://localhost:8000
   API Docs: http://localhost:8000/docs
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop services:**
   ```bash
   docker-compose down
   ```

## 📱 Modules

### 1. Finance (The Bag) 💰
- Transaction tracking
- Receipt OCR processing
- Budget management
- Runway calculation
- Subscription detection

### 2. Knowledge (The Brain) 🧠
- Knowledge CRUD operations
- Anki SRS integration
- Web clipping
- Worktree management
- Semantic search

### 3. Social (The Circle) 👥
- Contact management
- Health logging
- Mood tracking
- Check-in trends
- Reminders

### 4. Health (The Vessel) ❤️
- Blueprint protocol tracking
- Workout logging
- Biometric tracking
- Sobriety tracking
- Health analytics

## 🎨 Design System

### Colors
- **Primary:** Indigo (#6366f1)
- **Secondary:** Violet (#8b5cf6)
- **Accent:** Cyan (#06b6d4)
- **Success:** Emerald (#10b981)
- **Warning:** Amber (#f59e0b)
- **Error:** Red (#ef4444)

### Typography
- **Font:** Inter
- **Weights:** 300, 400, 500, 600, 700

### Icons
- **Library:** Material Design Icons
- **Usage:** Consistent icon language across modules

## 🔧 Configuration

### API Proxy

The frontend proxies API requests to the backend in development mode:

```javascript
// vite.config.js
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

Create a `.env` file in the `web-ui` directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 📊 State Management

Each module has its own Pinia store:

- `useBagStore` - Finance state
- `useBrainStore` - Knowledge state
- `useCircleStore` - Social state
- `useVesselStore` - Health state

Example usage:

```javascript
import { useBagStore } from '@/stores/bag'

const bagStore = useBagStore()
await bagStore.fetchTransactions()
```

## 🌐 API Integration

The frontend communicates with the backend via RESTful APIs:

```javascript
import { bagAPI } from '@/api'

// Get transactions
const transactions = await bagAPI.getTransactions({ limit: 50 })

// Create transaction
const result = await bagAPI.createTransaction({ ... })
```

## 📱 Responsive Breakpoints

- **xs:** < 600px (mobile)
- **sm:** 600px - 960px (tablet)
- **md:** 960px - 1280px (laptop)
- **lg:** 1280px - 1920px (desktop)
- **xl:** > 1920px (large desktop)

## 🔐 Authentication

Currently uses test authentication via headers. Update the API interceptor for production:

```javascript
// src/api/index.js
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('nexus-token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## 🚀 Deployment

### Cloudflare Tunnel (Recommended)

1. Build the Docker images
2. Run with Docker Compose
3. Configure Cloudflare Tunnel to route:
   - `nexus.yourdomain.com` → localhost:5173
   - `nexus-api.yourdomain.com` → localhost:8000

### Direct Deployment

1. Build the frontend:
   ```bash
   cd web-ui
   npm run build
   ```

2. Build the backend Docker image:
   ```bash
   docker build -f Dockerfile.api -t nexus-api .
   ```

3. Run with Docker Compose or deploy to your preferred platform

## 🧪 Testing

```bash
# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e

# Lint code
npm run lint

# Format code
npm run format
```

## 📝 Development Notes

### Adding a New Feature

1. Create the API endpoint in the backend
2. Add the API client method in `src/api/index.js`
3. Create or update the store in `src/stores/`
4. Update the view component in `src/views/`
5. Test on multiple screen sizes

### State Management Best Practices

- Keep stores focused and single-purpose
- Use computed properties for derived state
- Handle errors gracefully with try-catch
- Show loading states during async operations
- Use optimistic updates where appropriate

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT

## 👥 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API docs at `/docs`

---

Built with ❤️ using Vue 3 + FastAPI
