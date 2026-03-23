import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: '/LEGEND-STAR/',
  plugins: [react()],
  server: {
    port: 5173,
  },
});
