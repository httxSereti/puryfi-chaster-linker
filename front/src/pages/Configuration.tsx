import { Settings, Save } from "lucide-react";

export default function Configuration() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-[rgb(36,34,45)] text-slate-100 p-4 font-sans">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden p-8 transition-all hover:shadow-cyan-900/20">
        <div className="flex flex-col items-center text-center space-y-6">

          <div className="p-4 bg-cyan-950/30 rounded-full border border-cyan-900/50 shadow-inner">
            <Settings className="w-10 h-10 text-cyan-400" />
          </div>

          <div className="space-y-2">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Configuration
            </h1>
            <p className="text-sm text-slate-400">
              Puryfi Chaster Linker Settings
            </p>
          </div>

          <div className="w-full h-[1px] bg-slate-800" />

          <div className="w-full space-y-4">
            {/* Exemple de champ de configuration */}
            <div className="space-y-2 text-left">
              <label className="text-sm font-semibold text-slate-300">
                Lock ID
              </label>
              <input
                type="text"
                placeholder="Ex: lock_12345"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600 transition-shadow"
              />
            </div>

            <div className="space-y-2 text-left">
              <label className="text-sm font-semibold text-slate-300">
                Sync Mode
              </label>
              <select className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600 transition-shadow appearance-none">
                <option value="auto">Auto</option>
                <option value="manual">Manual</option>
              </select>
            </div>

            <button className="w-full mt-4 flex items-center justify-center gap-2 py-3 px-4 bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-semibold rounded-xl transition-all shadow-lg shadow-cyan-900/20 active:scale-95">
              <Save className="w-4 h-4" />
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
