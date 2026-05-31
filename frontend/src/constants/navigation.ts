import { Activity, Home, LayoutDashboard } from "lucide-react";
import { routes } from "./routes";
import type { NavigationItem } from "../types/navigation";

export const navigationItems: NavigationItem[] = [
  {
    label: "Home",
    path: routes.home,
    icon: Home,
  },
  {
    label: "Dashboard",
    path: routes.dashboard,
    icon: LayoutDashboard,
  },
  {
    label: "Analysis",
    path: routes.analysis,
    icon: Activity,
  },
];
