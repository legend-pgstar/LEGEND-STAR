/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#050A19',
        card: '#0D1330',
        neonblue: '#6EE7FF',
        neonpurple: '#C084FC',
      },
      boxShadow: {
        neon: '0 0 20px rgba(99, 102, 241, 0.35)',
      },
    },
  },
  plugins: [],
};
