/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#09090B',
        card: '#121215',
        cardBorder: 'rgba(255, 255, 255, 0.08)',
        cardHoverBorder: 'rgba(255, 255, 255, 0.22)',
      }
    },
  },
  plugins: [],
}
