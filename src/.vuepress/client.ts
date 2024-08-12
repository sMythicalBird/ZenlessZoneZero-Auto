import { defineClientConfig } from "vuepress/client";
import { setupTransparentNavbar } from "vuepress-theme-hope/presets/transparentNavbar.js";
import "vuepress-theme-hope/presets/hr-driving-car.scss"
import "vuepress-theme-hope/presets/bounce-icon.scss"
import "vuepress-theme-hope/presets/shinning-feature-panel.scss"

export default defineClientConfig({
  setup: () => {
    setupTransparentNavbar({ type: "homepage" });
  },
});