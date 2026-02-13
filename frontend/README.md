# Resume Apply - Frontend

Modern React + TypeScript + Tailwind CSS frontend for the Resume Apply application.

## Features

- 🎨 Beautiful, responsive UI built with Tailwind CSS
- ⚡ Fast development with Vite
- 📝 Full TypeScript support
- 🔄 Complete workflow implementation:
  - Flow selection (Improve Resume / Apply to Jobs)
  - Resume upload with drag & drop
  - Job URL input or improvement instructions
  - AI-powered results display
  - Iterative feedback loop

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
cd frontend
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

**Note:** Make sure the backend API is running on `http://localhost:8000`

### Build for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/        # React components
│   │   ├── FlowSelector.tsx    # Initial flow selection
│   │   ├── ResumeUpload.tsx    # Resume upload UI
│   │   ├── JobInput.tsx        # Job URLs / improvement notes
│   │   ├── Results.tsx         # Display AI results
│   │   └── Feedback.tsx        # Feedback and iteration UI
│   ├── services/          # API client
│   │   └── api.ts
│   ├── types/             # TypeScript types
│   │   └── api.ts
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

## API Integration

The frontend communicates with the backend API via the `/api` proxy configured in `vite.config.ts`. All API calls are handled through `src/services/api.ts`.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Design System

### Colors

- Primary: `#0EA5E9` (sky-500)
- Dark: `#0F172A` (slate-900)
- Muted: `#64748B` (slate-500)

### Components

All components follow a consistent design pattern with:
- Rounded corners and shadows
- Smooth transitions
- Hover states
- Loading states
- Error handling

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
