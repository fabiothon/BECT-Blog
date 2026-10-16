import { showModal } from "/static/js/utils.js";

const THEME_LABELS = { light: "☀︎ Light", dark: "☾ Dark", auto: "◐ Auto" };
const darkQuery = window.matchMedia("(prefers-color-scheme: dark)");

function storedTheme() {
  return localStorage.getItem("theme") || "auto";
}

function applyTheme(theme) {
  const dark = theme === "dark" || (theme === "auto" && darkQuery.matches);
  document.documentElement.classList.toggle("dark", dark);
  document.getElementById("themeLabel").textContent = THEME_LABELS[theme];
  document.querySelectorAll("[data-theme-value]").forEach((option) => {
    option.setAttribute(
      "aria-checked",
      String(option.dataset.themeValue === theme),
    );
  });
}

export function initDialogs() {
  let pressedOnBackdrop = false;

  document.addEventListener("pointerdown", (event) => {
    pressedOnBackdrop = event.target instanceof HTMLDialogElement;
  });

  document.addEventListener("click", (event) => {
    const opener = event.target.closest("[data-dialog-open]");
    if (opener) {
      showModal(opener.dataset.dialogOpen);
      return;
    }

    const closer = event.target.closest("[data-dialog-close]");
    if (closer) {
      closer.closest("dialog")?.close();
      return;
    }

    if (pressedOnBackdrop && event.target instanceof HTMLDialogElement) {
      event.target.close();
    }
  });
}

export function initNavToggle() {
  const toggle = document.getElementById("navToggle");
  const menu = document.getElementById("navMenu");

  toggle.addEventListener("click", () => {
    const open = menu.dataset.open !== "true";
    menu.dataset.open = String(open);
    toggle.setAttribute("aria-expanded", String(open));
  });
}

export function initThemeMenu() {
  const toggle = document.getElementById("themeToggle");
  const menu = document.getElementById("themeMenu");

  const setOpen = (open) => {
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  };

  toggle.addEventListener("click", () => setOpen(menu.hidden));

  menu.addEventListener("click", (event) => {
    const option = event.target.closest("[data-theme-value]");
    if (!option) return;
    localStorage.setItem("theme", option.dataset.themeValue);
    applyTheme(option.dataset.themeValue);
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (event) => {
    if (!menu.hidden && !event.target.closest("#themeToggle, #themeMenu")) {
      setOpen(false);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !menu.hidden) {
      setOpen(false);
      toggle.focus();
    }
  });

  darkQuery.addEventListener("change", () => {
    if (storedTheme() === "auto") applyTheme("auto");
  });

  applyTheme(storedTheme());
}
