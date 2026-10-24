import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}"],
  theme: { extend: { colors: { ink: "#10151b", panel: "#171e26", mint: "#9fe870", amber: "#f4b942" }, fontFamily: { sans: ["var(--font-geist)"] } } },
  plugins: [],
};
export default config;
