import {
  DashboardCustomize,
  QuestionAnswer,
  Report,
} from "@mui/icons-material";
import { createTheme } from "@mui/material";

import {
  AppProvider,
  DashboardLayout,
  Navigation,
  PageContainer,
  PageContainerToolbar,
  Router,
} from "@toolpad/core";
import React from "react";
import { HashRouter, Route, Routes } from "react-router-dom";
import { Dashboard, Reports } from "./components/pages/admin";
import { Interviews } from "./components/pages/common/Interviews";

// const App = () => {
//   return (
//     <HashRouter>
//       <Layout>
//         <Routes>
//           <Route path="/" element={<Home />} />
//           <Route path="/interviews" element={<Interviews />} />
//         </Routes>
//       </Layout>
//     </HashRouter>
//   );
// };

const NAVIGATION: Navigation = [
  {
    kind: "header",
    title: "DeepFER",
  },
  {
    segment: "",
    title: "Dashboard",
    icon: <DashboardCustomize />,
  },
  {
    segment: "interviews",
    title: "Interviews",
    icon: <QuestionAnswer />,
  },
  {
    segment: "reports",
    title: "Reports",
    icon: <Report />,
  },
];

const BRANDING = {
  title: "WSPC",
};

const determineThemeMode = () => {
  const toolpadMode = localStorage.getItem("mui-toolpad-mode");
  const systemMode = window.matchMedia("(prefers-color-scheme: dark)").matches;

  const isToolpadModeUnseted = !toolpadMode || toolpadMode === "system";

  const useSystemDarkMode = isToolpadModeUnseted && systemMode;

  const themeMode = useSystemDarkMode
    ? "dark"
    : (toolpadMode as "light" | "dark");

  localStorage.setItem("mui-toolpad-mode", themeMode);
  return themeMode;
};

const theme = createTheme({
  cssVariables: {
    colorSchemeSelector: "data-toolpad-color-scheme",
  },
  colorSchemes: { light: true, dark: true },
  palette: {
    mode: determineThemeMode(),
  },
});

const App = () => {
  const [pathname, setPathname] = React.useState(
    window.location.hash.slice(1) ?? "/"
  );

  React.useEffect(() => {
    const handlePathnameChange = () => {
      setPathname(window.location.hash.slice(1) ?? "/");
    };
    window.addEventListener("popstate", handlePathnameChange);

    return () => {
      window.removeEventListener("popstate", handlePathnameChange);
    };
  }, []);

  const router = React.useMemo<Router>(() => {
    return {
      pathname,
      searchParams: new URLSearchParams(),
      navigate: (path) => {
        setPathname(String(path));
        window.location.hash = `#${path}`;
      },
    };
  }, [pathname]);

  return (
    <HashRouter>
      <AppProvider
        navigation={NAVIGATION}
        branding={BRANDING}
        theme={theme}
        router={router}
      >
        <DashboardLayout>
          <PageContainer slots={{ toolbar: PageContainerToolbar }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/interviews" element={<Interviews />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </PageContainer>
        </DashboardLayout>
      </AppProvider>
    </HashRouter>
  );
};

export default App;
