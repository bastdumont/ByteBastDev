/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        base: {
          blue: '#0052FF',
          dark: '#000000',
          light: '#FFFFFF',
        },
      },
    },
  },
  plugins: [],
}
