import { Link } from "react-router-dom";

export function Header() {
  return (
    <header className="h-16 border-b border-gray-800 bg-[#0B1220] flex items-center justify-between px-6">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
          <span className="text-black font-bold">A</span>
        </div>
        <Link to="/" className="text-white font-bold text-xl tracking-wider">AEGIS EARTH</Link>
      </div>
      <nav className="flex items-center gap-6">
        <Link to="/dashboard" className="text-gray-300 hover:text-primary transition-colors">Dashboard</Link>
        <button className="text-gray-300 hover:text-white transition-colors">
          Settings
        </button>
      </nav>
    </header>
  );
}
