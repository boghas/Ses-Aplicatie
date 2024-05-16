import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    'import.meta.env': JSON.stringify(process.env),
  },
  server: {
    host: '0.0.0.0',
  },
  plugins: [react()],
})
