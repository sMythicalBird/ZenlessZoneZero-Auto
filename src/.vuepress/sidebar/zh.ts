import { sidebar } from "vuepress-theme-hope";

export const zhSidebar = sidebar({
  "/zh/": [
    "",
    {
      text: "快速入门",
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
      text: "用户社区",
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
