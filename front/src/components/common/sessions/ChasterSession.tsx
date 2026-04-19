import type { ChasterExtensionSessionSchema } from "@/types/api";
import ChasterKeyholderSession from "./keyholder/ChasterKeyholderSession";
import ChasterWearerSession from "./wearer/ChasterWearerSession";

export default function ChasterSession({ session }: { session: ChasterExtensionSessionSchema }) {

    if (!session) {
        return (
            <div>
                <h1>No Chaster Session</h1>
            </div>
        );
    }

    return (
        <div className="w-full space-y-4">
            <div className="w-full p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
                {session.role === "keyholder" ? (
                    <ChasterKeyholderSession session={session} />
                ) : (
                    <ChasterWearerSession session={session} />
                )}
            </div>
        </div>
    );
}