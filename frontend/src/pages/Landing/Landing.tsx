import { Link } from "react-router-dom";

export function Landing() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-7rem)] px-4">
      <div className="max-w-3xl text-center space-y-8">
        <div className="w-24 h-24 rounded-full bg-primary mx-auto flex items-center justify-center mb-8 shadow-[0_0_40px_rgba(0,229,168,0.3)]">
          <span className="text-black font-bold text-4xl">A</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white">
          AEGIS EARTH
        </h1>
        
        <p className="text-xl md:text-2xl text-primary font-medium tracking-widest uppercase">
          Observe. Analyze. Protect.
        </p>
        
        <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
          The next-generation disaster intelligence platform. Aegis Earth aggregates satellite imagery, real-time telemetry, and advanced risk scoring models to predict and track global hazards before they escalate.
        </p>
        
        <div className="pt-8">
          <Link 
            to="/dashboard" 
            className="inline-flex items-center justify-center px-8 py-4 bg-primary text-black font-semibold rounded-md hover:bg-primary/90 transition-all hover:scale-105 shadow-[0_0_20px_rgba(0,229,168,0.2)]"
          >
            Access Intelligence Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}
