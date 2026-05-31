import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#06111f",
        foreground: "#e7eef8",
        border: "rgba(148, 163, 184, 0.22)",
        card: "rgba(10, 24, 42, 0.82)",
        muted: "#8aa0b8",
        primary: "#49d3b4",
        warning: "#f2b84b",
        danger: "#ff6b6b",
        signal: "#7dd3fc",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      boxShadow: {
        "aegis-panel": "0 24px 70px rgba(0, 0, 0, 0.32)",
      },
    },
  },
  plugins: [],
};

export default config;

