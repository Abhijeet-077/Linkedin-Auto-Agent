import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  // GitHub Pages deployment configuration
  base: mode === 'production' ? '/linkedin-forge-AutoAgent/' : '/',
  server: {
    host: "::",
    port: 8080,
  },
  plugins: [
    react(),
    mode === 'development' &&
    componentTagger(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu', '@radix-ui/react-toast'],
          router: ['react-router-dom'],
          motion: ['framer-motion'],
          charts: ['recharts'],
          query: ['@tanstack/react-query'],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
    // Ensure proper asset handling for GitHub Pages
    sourcemap: false,
    minify: 'esbuild',
  },
  // Define environment variables for different modes
  define: {
    __GITHUB_PAGES__: mode === 'production',
  },
}));
