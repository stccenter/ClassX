import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  server: {
    proxy: {
      // '/api': "http://localhost:8080",
      '/api': 'http://localhost:5000',
    },
  },
  plugins: [
    react({
      jsxImportSource: "@emotion/react",
      babel: {
        plugins: ["@emotion/babel-plugin"],
      },
    }),
  ],
  optimizeDeps: {
    include: ['@emotion/react'],
  },
  build: {
    rollupOptions: {
      external: [],
    }
  }
});
