import { useState } from "react";
import type { ChasterExtensionSessionSchema } from "@/types/api";
import { ShieldCheck } from "lucide-react";
import LinkTokenModal from "./LinkTokenModal";

export default function ChasterWearerSession({ session }: { session: ChasterExtensionSessionSchema }) {
    const [modalOpen, setModalOpen] = useState(false);
    const [linkToken, setLinkToken] = useState<string | null>(session.link_token ?? null);

    if (!session) {
        return (
            <div>
                <h1>No Chaster Session</h1>
            </div>
        );
    }

    return (
        <>
            <div className="flex flex-col gap-2 text-left">
                <div className="flex items-center justify-between">
                    <div className="flex flex-row gap-2 items-center">
                        <ShieldCheck className="w-5 h-5 text-slate-400" />
                        <p className="text-sm font-medium text-slate-300">Puryfi Link</p>
                    </div>

                    {session.is_linked ? (
                        <span className="text-sm font-semibold text-emerald-400">Linked</span>
                    ) : (
                        <button
                            onClick={() => setModalOpen(true)}
                            className="text-sm font-semibold text-red-400 hover:text-red-300 underline underline-offset-2 transition-colors"
                        >
                            Not linked
                        </button>
                    )}
                </div>
            </div>

            {modalOpen && (
                <LinkTokenModal
                    sessionId={session.id}
                    linkToken={linkToken}
                    onClose={() => setModalOpen(false)}
                    onTokenCreated={(token) => setLinkToken(token)}
                />
            )}
        </>
    );
}