import { lazy, Suspense } from "react";
import { Route, Routes } from "react-router-dom";
const Dashboard = lazy(() => import("./components/pages/admin/Dashboard"));
const Interviews = lazy(() => import("./components/pages/common/Interviews"));
const Reports = lazy(() => import("./components/pages/admin/Reports"));

const ROUTES = [
  {
    path: "/",
    element: () => <Dashboard />,
  },
  {
    path: "/interviews/",
    element: () => <Interviews />,
  },
  {
    path: "/interviews/:id",
    element: () => <Interviews />,
  },
  {
    path: "/reports",
    element: () => <Reports />,
  },
];

export default function AppRoutes() {
  return (
    <Routes>
      {ROUTES.map(({ path, element: Page }) => (
        <Route
          key={path}
          path={path}
          element={
            <Suspense>
              <Page />
            </Suspense>
          }
        />
      ))}
    </Routes>
  );
}
