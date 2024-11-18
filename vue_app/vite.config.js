import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import basicSSL from "@vitejs/plugin-basic-ssl";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode, ssrBuild })=>{
  const env = loadEnv(mode, process.cwd());
  return {
    define: {
      'process.env': {
        VITE_API_URL: env.VITE_API_URL
      }
    },
    plugins: [
      vue(),
      basicSSL()
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server:{
      host: '0.0.0.0',
      https: true
    }
  }
})
