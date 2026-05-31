export function Footer() {
  return (
    <footer className="h-12 border-t border-gray-800 bg-[#0B1220] flex items-center justify-between px-6 text-sm text-gray-500">
      <span>&copy; {new Date().getFullYear()} Aegis Earth</span>
      <span>System Status: <span className="text-primary">Online</span></span>
    </footer>
  );
}
