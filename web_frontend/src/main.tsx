import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import { ErrorBoundary } from './components/ErrorBoundary';
import './index.css';

// Consider wrapping initialization in an async function
const initApp = async () => {
  try {
    const root = createRoot(document.getElementById('root')!);
    root.render(
      <StrictMode>
        <ErrorBoundary fallback={<div>Something went wrong</div>}>
          <App />
        </ErrorBoundary>
      </StrictMode>
    );
  } catch (error) {
    console.error('Failed to initialize application:', error);
    // Maybe render a fallback error UI
  }
};

initApp().catch(error => {
  console.error('Critical application error:', error);
  // Show a fatal error message to the user
});

window.addEventListener('unhandledrejection', event => {
  console.error('Unhandled promise rejection:', event.reason);
  // Prevent the default handler
  event.preventDefault();
});