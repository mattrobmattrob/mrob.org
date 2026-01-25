import { defineConfig } from "astro/config";
import { rehypeImageCaption } from "./src/plugins/rehype-image-caption";

export default defineConfig({
  site: "https://mrob.org",
  output: "static",
  markdown: {
    rehypePlugins: [rehypeImageCaption],
    shikiConfig: {
      theme: "github-light",
    },
  },
});
