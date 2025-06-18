import { createTheme } from "@mui/material";

const theme = createTheme({
  cssVariables: {
    colorSchemeSelector: "data-toolpad-color-scheme",
  },
  colorSchemes: { light: true, dark: true },
  palette: {
    mode: determineThemeMode(),
  },
});

function determineThemeMode() {
  const toolpadMode = localStorage.getItem("mui-toolpad-mode");
  const systemMode = window.matchMedia("(prefers-color-scheme: dark)").matches;

  const isToolpadModeUnseted = !toolpadMode || toolpadMode === "system";

  const useSystemDarkMode = isToolpadModeUnseted && systemMode;

  const themeMode = useSystemDarkMode
    ? "dark"
    : (toolpadMode as "light" | "dark");

  localStorage.setItem("mui-toolpad-mode", themeMode);
  return themeMode;
}

export default theme;
