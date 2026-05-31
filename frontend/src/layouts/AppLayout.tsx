import { NavLink, Outlet } from "react-router-dom";
import { ShieldCheck } from "lucide-react";
import { navigationItems } from "../constants/navigation";
import { cn } from "../lib/utils";

export function AppLayout() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur-xl">
        <div className="mx-auto flex w-full max-w-7xl flex-col gap-4 px-5 py-4 lg:flex-row lg:items-center lg:justify-between">
          <NavLink to="/" className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-lg border border-primary/40 bg-primary/10">
              <ShieldCheck className="h-6 w-6 text-primary" aria-hidden="true" />
            </div>
            <div>
              <p className="text-lg font-bold text-foreground">Aegis Earth</p>
              <p className="text-sm text-muted">Observe. Analyze. Protect.</p>
            </div>
          </NavLink>

          <nav className="flex flex-wrap gap-2" aria-label="Primary navigation">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    cn(
                      "inline-flex h-10 items-center gap-2 rounded-md border px-3 text-sm font-semibold transition",
                      isActive
                        ? "border-primary/60 bg-primary/15 text-primary"
                        : "border-border bg-white/5 text-muted hover:bg-white/10 hover:text-foreground",
                    )
                  }
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {item.label}
                </NavLink>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="mx-auto w-full max-w-7xl px-5 py-6">
        <Outlet />
      </main>
    </div>
  );
}
