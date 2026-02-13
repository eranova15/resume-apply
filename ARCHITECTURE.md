# Frontend Architecture

## Component Hierarchy

```
App (Main State Manager)
├── Header (Logo, Navigation)
├── Main Content (Conditional Rendering)
│   ├── FlowSelector
│   │   └── Flow cards (Improve / Apply)
│   ├── ResumeUpload
│   │   └── Drag & Drop Area
│   ├── JobInput
│   │   ├── Multiple URL Inputs (Apply)
│   │   └── Change Notes Textarea (Improve)
│   ├── Results
│   │   ├── Tabs (Suggestions / Resume / Cover)
│   │   ├── Suggestions List
│   │   ├── Resume Preview
│   │   ├── Cover Letter Preview
│   │   └── Download Buttons
│   └── Feedback
│       ├── Feedback Options (Accept / Change / Improve)
│       ├── Resume Source Selector
│       └── Change Notes Input
└── Footer
```

## State Flow

```
┌─────────────────┐
│  FlowSelector   │ → User selects flow type
└────────┬────────┘
         ↓
    Create Session (API)
         ↓
┌─────────────────┐
│ ResumeUpload    │ → User uploads resume
└────────┬────────┘
         ↓
    Upload Resume (API)
         ↓
┌─────────────────┐
│   JobInput      │ → User provides input
└────────┬────────┘
         ↓
    Apply/Improve (API)
         ↓
┌─────────────────┐
│    Results      │ → Display AI output
└────────┬────────┘
         ↓
    User reviews
         ↓
┌─────────────────┐
│   Feedback      │ → User provides feedback
└────────┬────────┘
         ↓
    ┌───────────┐
    │  Accept?  │
    └─────┬─────┘
      Yes │ No
          │  ↓
          │ Feedback API
          │  ↓
          │ Back to Results (new version)
          ↓
      Complete
```

## App State

```typescript
type AppStep = 'flow' | 'upload' | 'input' | 'results' | 'feedback';

interface AppState {
  step: AppStep;                    // Current step in workflow
  flow: FlowType | null;            // 'improve' | 'apply'
  sessionId: string;                // Backend session ID
  result: EngineResponse | null;    // Latest AI results
  loading: boolean;                 // Loading state for async ops
}
```

## Data Flow

### Session Creation
```
FlowSelector → api.startSession(flow)
  ↓
{ session_id: "abc123" }
  ↓
App State (sessionId, flow)
```

### Resume Upload
```
ResumeUpload → api.uploadResume(sessionId, file)
  ↓
{ ok: true, filename: "resume.pdf", chars: 1500 }
  ↓
Navigate to Input Step
```

### Processing (Apply)
```
JobInput → api.apply({ session_id, job_urls })
  ↓
{
  session_id,
  iteration,
  suggestions: [...],
  improved_resume_text,
  cover_letter_text,
  resume_pdf_url,
  cover_letter_pdf_url
}
  ↓
Results Component
```

### Processing (Improve)
```
JobInput → api.improve({ session_id, change_notes })
  ↓
{ session_id, iteration, improved_resume_text, ... }
  ↓
Results Component
```

### Feedback Loop
```
Feedback → api.feedback({ 
  session_id, 
  choice, 
  change_notes,
  resume_source 
})
  ↓
New EngineResponse (iteration++)
  ↓
Back to Results
```

## Component Props

### FlowSelector
```typescript
interface FlowSelectorProps {
  onFlowSelect: (flow: FlowType, sessionId: string) => void;
}
```

### ResumeUpload
```typescript
interface ResumeUploadProps {
  sessionId: string;
  onUploadComplete: () => void;
}
```

### JobInput
```typescript
interface JobInputProps {
  sessionId: string;
  flow: FlowType;
  onProcessComplete: (result: EngineResponse) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}
```

### Results
```typescript
interface ResultsProps {
  result: EngineResponse;
  onShowFeedback: () => void;
}
```

### Feedback
```typescript
interface FeedbackProps {
  sessionId: string;
  currentResult: EngineResponse;
  onFeedbackComplete: (result: EngineResponse) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}
```

## API Service

```typescript
// services/api.ts
export const api = {
  startSession(flow): Promise<StartSessionResponse>
  uploadResume(sessionId, file): Promise<UploadResponse>
  apply(request): Promise<EngineResponse>
  improve(request): Promise<EngineResponse>
  feedback(request): Promise<EngineResponse>
  getDownloadUrl(filename): string
}
```

## Type Definitions

```typescript
// types/api.ts
type FlowType = 'improve' | 'apply';
type FeedbackChoice = 'accept' | 'change' | 'improve';
type ResumeSource = 'old' | 'new';

interface Suggestion {
  section: string;
  original: string;
  suggested: string;
  reason: string;
}

interface EngineResponse {
  session_id: string;
  iteration: number;
  suggestions: Suggestion[];
  improved_resume_text: string;
  cover_letter_text: string;
  resume_pdf_url: string | null;
  cover_letter_pdf_url: string | null;
}
```

## Routing Strategy

**Single-Page Application (SPA)** with conditional rendering:
- No React Router needed (simple linear flow)
- State-based navigation via `step` variable
- Each step shows different component
- "Start Over" button resets to initial state

## Styling Approach

**Tailwind CSS Utility-First:**
- No custom CSS files (except global styles)
- Consistent design tokens via tailwind.config.js
- Responsive by default (mobile-first)
- Hover states and transitions on interactive elements
- Loading states with spinners
- Error states with colored alerts

**Color Palette:**
- Primary: `#0EA5E9` (sky-500)
- Dark: `#0F172A` (slate-900)
- Muted: `#64748B` (slate-500)
- Backgrounds: slate-50, slate-100
- Borders: slate-200, slate-300

## User Experience Patterns

### Loading States
- Spinner + descriptive text
- Disabled buttons during processing
- Info box explaining what's happening

### Error Handling
- Red bordered alert boxes
- Inline validation errors
- Graceful fallbacks
- Console logging for debugging

### Success Feedback
- Green checkmarks
- Smooth transitions between steps
- Progress indicators (iteration counter)
- Clear call-to-action buttons

### Interactive Elements
- Hover effects on all buttons/cards
- Active states for selections
- Smooth transitions (200-300ms)
- Focus outlines for accessibility

## Performance Considerations

- Lazy loading not needed (small app)
- Single bundle via Vite
- API calls use Axios (cancellation support available)
- No heavy computations on frontend
- Large text content in `<pre>` tags for performance

## Accessibility

- Semantic HTML elements
- Button vs link distinction
- Alt text for icons (via SR-only if needed)
- Focus states visible
- Color contrast ratios meet WCAG AA
- Keyboard navigation support

## Future Enhancements

Potential improvements (not implemented):
- [ ] Text highlighting/markup for specific changes
- [ ] Side-by-side diff view
- [ ] Export to DOCX format
- [ ] Resume template selection
- [ ] User authentication
- [ ] Session persistence (local storage)
- [ ] Undo/redo functionality
- [ ] Share results via link
