import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'


export default defineConfig({
  plugins: [vue()],
  define: { "process.env": {} },
  server: {
    port: 4000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
      },
      "/auth": {
        target: "http://localhost:8000",
      },
    },
  },
})