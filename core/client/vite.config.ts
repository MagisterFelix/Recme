import * as path from 'path';

import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [{ find: '@', replacement: path.resolve(__dirname, 'src') }],
  },
  build: {
    outDir: path.join(__dirname, 'build'),
    assetsDir: 'static',
  },
  server: {
    host: '127.0.0.1',
    port: 3000,
  },
});
