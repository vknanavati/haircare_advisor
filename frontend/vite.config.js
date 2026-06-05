// vite.config.js
// Configures Vite — the build tool and dev server for the React frontend.
// We tell it about Tailwind and set the proxy so API calls to /search
// get forwarded to our Flask backend on port 5008.

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),        // enables React JSX transformation
    tailwindcss(),  // enables Tailwind CSS utility classes
  ],
  server: {
    proxy: {
      // any request from React starting with /api gets forwarded to Flask
      // so instead of calling http://localhost:5008/search directly,
      // React calls /api/search and Vite handles the forwarding
      '/api': {
        target: 'http://localhost:5008',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})