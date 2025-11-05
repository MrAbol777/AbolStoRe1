/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  darkMode: 'class', // Add this line to enable dark mode
  theme: {
    extend: {
      fontFamily: {
        'iran-yekan': ['IranYekan', 'Vazirmatn', 'sans-serif'],
        'sf-pro-display': ['SF Pro Display', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
        'montserrat': ['Montserrat', 'sans-serif'],
      },
      colors: {
        'very-dark-bg': '#0b0b10',
        'dark-navy': '#0A0A1E',
        'glossy-black': '#03030C',
        'accent-orange': '#ff7a00', // Primary neon/CTA orange
        'neon-golden': '#ffb300', // Primary neon/CTA golden
        'neon-light-orange': '#ffd58a', // Secondary glow/highlight
        'light-text': 'rgba(255,255,255,0.65)',
        'vibrant-orange': '#FFA500', // Even brighter orange
        'bright-orange': '#FFD700', // Golden color
        'golden': '#FFC107', // Another golden shade
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
        '4xl': '2.5rem',
        '5xl': '3rem',
      },
      boxShadow: {
        'orange-glow': '0 0 15px rgba(255, 122, 0, 0.6), 0 0 30px rgba(255, 122, 0, 0.3)', // Updated neon glow
        'orange-light': '0 0 30px rgba(255, 165, 0, 0.3), 0 0 60px rgba(255, 165, 0, 0.15)', // Softer light
        'liquid-glass': 'inset 0 0 10px rgba(255,255,255,0.6), 0 0 20px rgba(255,255,255,0.3)', // Initial liquid glass effect
        'neon-glow': '0 0 5px #ff7a00, 0 0 10px #ff7a00, 0 0 20px #ff7a00, 0 0 40px #ffb300',
      },
      textShadow: {
        'default': '0 1px 2px rgba(0, 0, 0, 0.1)',
        'md': '0 3px 6px rgba(0, 0, 0, 0.15)',
        'lg': '0 5px 10px rgba(0, 0, 0, 0.2)',
        'neon-glow': '0 0 5px #ff7a00, 0 0 10px #ff7a00',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%': { 'background-position': '-200% 0' },
          '100%': { 'background-position': '200% 0' },
        },
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '.5' },
        },
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.5s ease-out forwards',
        'shimmer': 'shimmer 3s infinite linear',
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        animationDelay: {
          '100': '100ms',
          '200': '200ms',
          '300': '300ms',
          '400': '400ms',
          '500': '500ms',
          '600': '600ms',
          '700': '700ms',
          '800': '800ms',
          '900': '900ms',
          '1000': '1000ms',
        },
      },
    },
  },
  plugins: [
    function ({ matchUtilities, theme }) {
      matchUtilities(
        {
          'animation-delay': (value) => ({
            'animation-delay': value,
          }),
        },
        { values: theme('animationDelay') }
      )
    },
    function ({ addUtilities, theme }) {
      const newUtilities = {
        '.text-shadow': {
          'text-shadow': theme('textShadow.default'),
        },
        '.text-shadow-md': {
          'text-shadow': theme('textShadow.md'),
        },
        '.text-shadow-lg': {
          'text-shadow': theme('textShadow.lg'),
        },
        '.text-shadow-none': {
          'text-shadow': 'none',
        },
        '.text-shadow-neon-glow': {
          'text-shadow': theme('textShadow.neon-glow'),
        },
      }
      addUtilities(newUtilities, ['responsive', 'hover'])
    },
  ],
}