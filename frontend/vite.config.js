import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const isGithubPages = process.env.GITHUB_PAGES === "true";

export default defineConfig({
  plugins: [react()],
  base: isGithubPages ? "/truck-trip-details/" : "/",
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
