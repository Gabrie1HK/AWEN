import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/tests/setup.js'],
    include: ['src/**/*.test.{js,jsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: [
        'src/pages/ParcelManagement.jsx',
        'src/pages/Logistics.jsx',
        'src/pages/ProofOfDelivery.jsx',
        'src/pages/Reports.jsx',
        'src/pages/Dashboard.jsx',
        'src/pages/ClientProfile.jsx',
        'src/pages/DriverDashboard.jsx',
        'src/hooks/**/*.js',
        'src/context/**/*.{js,jsx}',
      ],
      thresholds: {
        'src/pages/**/*.jsx': {
          statements: 70,
          branches: 50,
        },
        'src/hooks/**/*.js': {
          functions: 80,
          lines: 70,
        },
        'src/context/**/*.{js,jsx}': {
          functions: 80,
          lines: 70,
        },
      },
    },
  },
})
