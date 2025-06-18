import {
  DashboardCustomize,
  QuestionAnswer,
  Report,
} from "@mui/icons-material";

import {
  AppProvider,
  DashboardLayout,
  Navigation,
  Router,
} from "@toolpad/core";
import React from "react";
import { HashRouter } from "react-router-dom";
import AppRoutes from "./routes";
import theme from "./theme";

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
    pattern: "interviews{/:call}?",
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
          <AppRoutes />
        </DashboardLayout>
      </AppProvider>
    </HashRouter>
  );
};

export default App;
