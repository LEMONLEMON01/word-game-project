## Tylmus Frontend — Project Instructions

Vue 3 + TypeScript application with Pinia for state management. Communicates with backend API via Axios.

### Project Structure
frontend/
├── src/
│   ├── api/
│   │   └── gameApi.ts          # Axios instance, API methods
│   ├── components/
│   │   ├── CategoryBlock.vue
│   │   ├── GameControls.vue
│   │   ├── GameHeader.vue
│   │   ├── MessageAlert.vue
│   │   ├── NotificationPopup.vue
│   │   └── WordCard.vue
│   ├── router/
│   │   └── index.ts             # Vue Router configuration
│   ├── stores/
│   │   ├── counter.ts           # Example store (can be removed)
│   │   └── gameStore.ts          # Main game state (Pinia)
│   ├── types/
│   │   └── game.ts               # TypeScript interfaces
│   ├── views/
│   │   └── GameView.vue           # Main game view
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── public/
├── index.html
├── package.json
├── vite.config.ts
├── Dockerfile                     # Multi-stage build with nginx
├── nginx.conf                      # SPA routing
├── .env                            # VITE_* environment variables

### Code Style
- Vue 3 Composition API with <script setup lang="ts">.
- Follow Vue Style Guide (priority A & B rules).
- **Filenaming**: PascalCase for components, camelCase for utility files.
- TypeScript: strict mode enabled; use interfaces from types/game.ts.
- Pinia stores: use defineStore with arrow functions and ref`/`computed.
- Imports: organized by type (e.g., Vue, Pinia, components, types).

### State Management
- Game state is centralized in gameStore.ts.
- Store actions for API calls (`initializeGame`, `submitGuess`), mutations for local updates.
- Use localStorage to persist attempt history across page reloads (implemented in store).

### API Communication
- Axios instance in gameApi.ts with base URL from import.meta.env.VITE_API_BASE_URL.
- withCredentials: true to include cookies for session tracking.
- All API errors caught and displayed via MessageAlert`/`NotificationPopup.
- Log API calls in development using console.log (remove in production).

### Testing
- Vitest for unit tests (if added).
- Test Pinia store actions by mocking API responses.
- Naming: *.spec.ts.

### Deployment
- Docker: multi-stage build.
  - Build stage: node:18-alpine, run npm ci and npm run build.
  - Production stage: nginx:alpine, copy dist/ to nginx html folder, use custom nginx.conf to handle SPA routing (try_files).
- Expose port 80.
- Environment variables are baked at build time; for runtime config, consider using window.ENV or a config file.
