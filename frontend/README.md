# PromptLab Frontend

PromptLab frontend is a React + Vite application for managing prompts and collections through a FastAPI backend.

## Features

- View all prompts with search and filtering
- Create, edit, and delete prompts
- View detailed prompt information
- Create and manage collections
- Delete collections
- Assign prompts to collections
- Add comma-separated tags
- Filter prompts by collection
- Search prompts by title, content, or description
- Connect to FastAPI backend with proper error handling
- Loading states for async operations

## Tech Stack

- React 18 with Hooks
- Vite for fast development and build
- ESLint for code quality
- Modular component architecture
- Organized API layer with separate modules

## Prerequisites

- Node.js 16+ and npm
- Python 3.9+ (for backend)
- FastAPI backend running

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `frontend/.env` with:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

**Note:** Change the URL if your backend runs on a different host or port.

### 3. Start the Backend

In a separate terminal:

```bash
cd backend
uvicorn app.api:app --reload
```

The backend will run at `http://127.0.0.1:8000`

### 4. Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will run at `http://localhost:5173`

### 5. Open in Browser

Navigate to `http://localhost:5173` and start creating prompts!

## Development

### Run Development Server

```bash
npm run dev
```

Vite will automatically reload on file changes.

### Lint Code

```bash
npm run lint
```

Run ESLint to check for code quality issues.

### Build for Production

```bash
npm run build
```

Generates an optimized build in the `dist/` folder.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable React components
│   │   ├── Layout.jsx
│   │   ├── Header.jsx
│   │   ├── PromptForm.jsx
│   │   ├── PromptList.jsx
│   │   ├── PromptCard.jsx
│   │   ├── PromptDetail.jsx
│   │   ├── CollectionForm.jsx
│   │   ├── CollectionList.jsx
│   │   ├── SearchBar.jsx
│   │   ├── LoadingSpinner.jsx
│   │   ├── Button.jsx
│   │   ├── Modal.jsx
│   │   ├── ErrorMessage.jsx
│   │   └── index.js
│   ├── api/               # API client modules
│   │   ├── client.js      # Base HTTP utility
│   │   ├── prompts.js     # Prompt endpoints
│   │   ├── collections.js # Collection endpoints
│   │   └── index.js       # Central export
│   ├── App.jsx            # Main app component
│   ├── App.css            # Global styles
│   ├── index.css          # Reset and base styles
│   └── main.jsx           # React entry point
├── public/                # Static assets
├── package.json
├── vite.config.js
└── eslint.config.js
```

## API Integration

The frontend connects to a FastAPI backend with the following endpoints:

### Prompts
- `GET /prompts` - Get all prompts
- `GET /prompts/{id}` - Get a single prompt
- `POST /prompts` - Create a new prompt
- `PUT /prompts/{id}` - Update a prompt
- `DELETE /prompts/{id}` - Delete a prompt

### Collections
- `GET /collections` - Get all collections
- `POST /collections` - Create a collection
- `DELETE /collections/{id}` - Delete a collection

## Troubleshooting

### Frontend won't load

1. **Check Node.js version:**
   ```bash
   node --version
   npm --version
   ```
   Ensure Node.js 16+ is installed.

2. **Clear cache and reinstall:**
   ```bash
   rm -r node_modules package-lock.json
   npm install
   ```

### Backend connection errors

1. **CORS errors:** The backend must have CORS configured to accept requests from `http://localhost:5173`

2. **API_BASE_URL not correct:**
   - Check `frontend/.env` and verify the backend URL
   - Default: `http://127.0.0.1:8000`

3. **Backend not running:**
   ```bash
   cd backend
   uvicorn app.api:app --reload
   ```
   Verify the server is running on the configured port.

4. **Port already in use:**
   - Frontend: Change Vite port in `vite.config.js`
   - Backend: Run on different port with `--port 8001`

### Loading/Rendering issues

1. **Clear browser cache:**
   - DevTools → Application → Clear storage
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

2. **Check browser console:**
   - Press `F12` to open DevTools
   - Check the Console tab for JavaScript errors
   - Check the Network tab to verify API requests

### ESLint errors

Fix linting issues automatically:

```bash
npm run lint -- --fix
```

## Environment Variables

Create `frontend/.env`:

```env
# Backend API URL (required)
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### Alternative backends

- Local: `http://127.0.0.1:8000`
- Remote: `https://api.example.com`
- Docker: `http://backend:8000` (if using docker-compose)

## Performance Tips

1. **Use browser DevTools Lighthouse** to audit performance
2. **Check Network tab** to ensure API requests are efficient
3. **Monitor console** for unnecessary re-renders
4. **Build size:** Run `npm run build` and check the `dist/` folder

## Contributing

- Follow existing code structure and naming conventions
- Keep components small and focused
- Document complex logic with JSDoc comments
- Run `npm run lint` before committing

## Additional Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [ESLint Documentation](https://eslint.org)

## Week 4 Requirement Checklist

| Requirement | Status |
|---|---|
| Prompt list view | Completed |
| Create prompt | Completed |
| Edit prompt | Completed |
| Delete prompt | Completed |
| Collection create/view | Completed |
| Assign prompt to collection | Completed |
| Comma-separated tags | Completed |
| FastAPI backend integration | Completed |
| Vite production build | Completed |