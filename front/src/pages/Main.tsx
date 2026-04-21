import { useEffect, useState } from "react";
import { Loader2, Eye, EyeOff, Copy, Check } from "lucide-react";
import axios from "axios";

import type { ChasterExtensionSessionSchema } from "@/types/api";
import ChasterSession from "@/components/common/sessions/ChasterSession";

export default function Main() {
  const [sessionData, setSessionData] = useState<ChasterExtensionSessionSchema | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopyPassword = () => {
    if (sessionData?.lock_password) {
      navigator.clipboard.writeText(sessionData.lock_password);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  useEffect(() => {
    const fetchSession = async () => {
      try {
        if (!window.location.hash) {
          throw new Error("No login token detected in URL.");
        }

        const hash = window.location.hash.substring(1);
        const params = JSON.parse(decodeURIComponent(hash));

        if (!params.mainToken) {
          throw new Error("mainToken not found in parameters.");
        }

        const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://localhost:8090";
        const response = await axios.get(`${backendUrl}/api/extensions/auth/sessions/${params.mainToken}`);
        setSessionData(response.data);
      } catch (err: any) {
        if (axios.isAxiosError(err)) {
          setError(err.response?.data?.detail || "Error syncing with local server.");
        } else {
          setError(err.message || "Error parsing parameters");
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchSession();
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen bg-[rgb(36,34,45)] text-slate-100 p-4 font-sans">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden p-8 transition-all hover:shadow-cyan-900/20">
        <div className="flex flex-col items-center text-center space-y-6">

          <div className="p-4 bg-cyan-950/30 rounded-full border border-cyan-900/50 shadow-inner">
            <img src="/logo.png" alt="Puryfi Chaster Linker" className="w-10 h-10 object-contain" />
          </div>

          <div className="space-y-2">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Puryfi Chaster Linker
            </h1>
            <p className="text-sm text-slate-400">
              Sync your Chaster lock with Puryfi
            </p>
          </div>

          <div className="w-full h-[1px] bg-slate-800" />

          {error ? (
            <div className="w-full p-4 bg-red-950/50 border border-red-900/50 rounded-xl">
              <p className="text-sm text-red-400 font-medium">{error}</p>
            </div>
          ) : isLoading ? (
            <div className="flex flex-col items-center justify-center py-6 space-y-4">
              <Loader2 className="w-8 h-8 text-cyan-500 animate-spin" />
              <p className="text-sm text-slate-400 animate-pulse">Fetching session...</p>
            </div>
          ) : sessionData ? (
            <>
              <ChasterSession session={sessionData} />
              <div className="w-full mt-4 p-4 flex flex-col gap-2 bg-slate-950 border border-slate-800 rounded-xl text-left">
                <p className="text-xs font-semibold uppercase text-slate-500">Settings from Chaster Configuration</p>
                <div className="flex justify-between items-center bg-slate-900 border border-slate-700/50 p-2 px-3 rounded-lg">
                  <span className="text-sm text-slate-300">Lock on Freeze</span>
                  {sessionData.lock_on_freeze ? (
                    <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">Enabled</span>
                  ) : (
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Disabled</span>
                  )}
                </div>
                <div className="flex justify-between items-center bg-slate-900 border border-slate-700/50 p-2 px-3 rounded-lg">
                  <span className="text-sm text-slate-300">Unlock on Unfreeze</span>
                  {sessionData.unlock_on_unfreeze ? (
                    <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Enabled</span>
                  ) : (
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Disabled</span>
                  )}
                </div>
                {sessionData.lock_password && sessionData.role === "keyholder" && (
                  <div className="flex flex-col gap-2 bg-slate-900 border border-slate-700/50 p-3 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-300">Emergency Lock Password</span>
                      <button
                        onClick={() => setShowPassword(!showPassword)}
                        className="text-slate-400 hover:text-cyan-400 transition-colors flex items-center gap-1 text-xs font-medium bg-slate-800 px-2 py-1 rounded"
                      >
                        {showPassword ? (
                          <><EyeOff size={14} /> Ocult</>
                        ) : (
                          <><Eye size={14} /> Reveal</>
                        )}
                      </button>
                    </div>
                    {showPassword && (
                      <div className="flex justify-between items-center bg-black/40 p-2 rounded border border-slate-800 mt-1">
                        <span className="text-sm font-mono text-cyan-400 tracking-wider">
                          {sessionData.lock_password}
                        </span>
                        <button
                          onClick={handleCopyPassword}
                          className="text-slate-400 hover:text-emerald-400 transition-colors p-1"
                        >
                          {copied ? <Check size={16} className="text-emerald-400" /> : <Copy size={16} />}
                        </button>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
