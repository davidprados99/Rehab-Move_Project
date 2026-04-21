/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", 
  ],
  theme: {
    extend: {
      colors: {
        rehab: {
          light: '#F4F7F6',   
          primary: '#5DA7A3',
          secondary: '#7B88C3',
          dark: '#2D5A57',    
          accent: '#7B88C3',  
        }
      },
      borderRadius: {
        'rehab': '20px',
      }
    }
    },
  plugins: [],
}

