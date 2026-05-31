import { Navigate, Route, Routes } from "react-router-dom";
import { AppLayout } from "../layouts/AppLayout";
import { AnalysisPage } from "../pages/Analysis";
import { DashboardPage } from "../pages/Dashboard";
import { HomePage } from "../pages/Home";
import { NotFoundPage } from "../pages/NotFound";
import { routes } from "../constants/routes";

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="analysis" element={<AnalysisPage />} />
        <Route path="home" element={<Navigate to={routes.home} replace />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
