import { visit } from "unist-util-visit";

export function rehypeImageCaption() {
  return (tree: any) => {
    visit(tree, "element", (node, index, parent) => {
      if (
        node.tagName === "img" &&
        node.properties?.alt &&
        parent &&
        index !== undefined
      ) {
        const alt = node.properties.alt;

        // Skip if already inside a figure
        if (parent.tagName === "figure") return;

        // Create figcaption element
        const figcaption = {
          type: "element",
          tagName: "figcaption",
          properties: {},
          children: [{ type: "text", value: alt }],
        };

        // Create figure wrapper
        const figure = {
          type: "element",
          tagName: "figure",
          properties: {},
          children: [node, figcaption],
        };

        // Replace the image with the figure
        parent.children[index] = figure;
      }
    });
  };
}
