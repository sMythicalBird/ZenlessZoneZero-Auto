import { sidebar } from "vuepress-theme-hope";

export const enSidebar = sidebar({
  "/": [
    "",
    {
      text: "Get Start",
      icon: "laptop-code",
      prefix: "demo/",
      link: "demo/",
      children: [
        "required.md",
        "deploy.md",
        "configure.md"
      ]
    },

    {
      text: "Community",
      icon: "message",
      prefix: "community/",
      link: "community/",
      children: [
        "discuss.md",
        "bug.md",
        "problem.md",
        "updatelog.md"
      ]
    },
  ],
});
