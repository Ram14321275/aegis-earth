import { Outlet } from "react-router-dom";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";

export function RootLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-[#0B1220] text-white">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <main className="flex-1 overflow-auto">
          <Outlet />
        </main>
      </div>
      <Footer />
    </div>
  );
}
