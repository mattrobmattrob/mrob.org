import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://mrob.org",
  output: "static",
  markdown: {
    shikiConfig: {
      theme: "github-light",
    },
  },
});
