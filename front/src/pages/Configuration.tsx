import { useEffect, useState } from "react";
import { Loader2, Lock, ShieldCheck } from "lucide-react";
import axios from "axios";
import type { PartnerGetConfigurationAuthRepDto } from "@/types/chaster";

export default function Configuration() {
  const [configurationData, setConfigurationData] = useState<PartnerGetConfigurationAuthRepDto | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSession = async () => {
      try {
        if (!window.location.hash) {
          throw new Error("No login token detected in URL.");
        }

        const hash = window.location.hash.substring(1);
        const params = JSON.parse(decodeURIComponent(hash));

        if (!params.partnerConfigurationToken) {
          throw new Error("partnerConfigurationToken not found in parameters.");
        }

        const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://localhost:8090";
        const response = await axios.get(`${backendUrl}/api/extensions/configuration/${params.partnerConfigurationToken}`);
        setConfigurationData(response.data);
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
            <svg className="w-10 h-10 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
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
          ) : configurationData ? (
            <div className="w-full space-y-4">
              <div className="w-full p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
                <div className="flex items-center gap-3">
                  <ShieldCheck className="w-5 h-5 text-emerald-400" />
                  <p className="text-sm font-semibold text-slate-200">Session Synced</p>
                </div>
                <div className="grid grid-cols-2 gap-2 text-left">
                  <div>
                    <p className="text-xs text-slate-500 uppercase tracking-wider">Role</p>
                    <p className="text-sm font-medium text-slate-300 capitalize">{configurationData.user}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 uppercase tracking-wider">Config</p>
                    <p className="text-sm font-medium text-slate-300 capitalize">{JSON.stringify(configurationData.config)}</p>
                  </div>
                </div>
                <div className="text-left bg-slate-900 p-3 rounded-lg border border-slate-800">
                  <div className="flex items-center gap-2 mb-1">
                    <Lock className="w-4 h-4 text-cyan-500" />
                    <p className="text-xs text-slate-500 uppercase tracking-wider">Lock</p>
                  </div>
                  {/* <p className="text-sm font-mono text-cyan-300 truncate" title={configurationData.session.lock._id}>
                    {configurationData.session.lock._id}
                  </p> */}
                </div>
              </div>

              <button className="w-full py-3 px-4 bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-semibold rounded-xl transition-colors shadow-lg shadow-cyan-900/20 active:scale-95">
                Sync
              </button>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}