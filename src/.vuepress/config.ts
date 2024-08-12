import { defineUserConfig } from "vuepress";
import theme from "./theme.js";
import { redirectPlugin } from "vuepress-plugin-redirect";

export default defineUserConfig({
  base: "/",
  locales: {
    "/": {
      lang: "en-US",
      title: "ZonelessZero Automation Script",
      description: "A automatic brush script that allows you to liberate your hands",

    },
    "/zh/": {
      lang: "zh-CN",
      title: "绝区零自动化脚本",
      description: "一个让您解放双手的自动刷图脚本",
    },
  },
  theme,

  // Enable it with pwa
  // shouldPrefetch: false,
});
