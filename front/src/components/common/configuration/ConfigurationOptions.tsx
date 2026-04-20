import { Snowflake, Unlock } from "lucide-react";
import type { ChasterExtensionConfigSchema } from "@/types/chaster";
import ConfigurationSwitch from "./ConfigurationSwitch";

interface ConfigurationOptionsProps {
    config: ChasterExtensionConfigSchema;
    onChange: (updatedConfig: ChasterExtensionConfigSchema) => void;
}

export default function ConfigurationOptions({ config, onChange }: ConfigurationOptionsProps) {
    const handleToggle = (field: keyof ChasterExtensionConfigSchema) => {
        onChange({
            ...config,
            [field]: !config[field],
        });
    };

    return (
        <div className="flex flex-col gap-4 mt-4 w-full">
            <ConfigurationSwitch
                icon={<Snowflake className="w-5 h-5 text-cyan-400" />}
                title="Lock on Freeze"
                description="Automatically lock Puryfi when lock is frozen"
                checked={config.lock_on_freeze}
                onChange={() => handleToggle("lock_on_freeze")}
                baseColor="cyan"
            />

            <ConfigurationSwitch
                icon={<Unlock className="w-5 h-5 text-emerald-400" />}
                title="Unlock on Unfreeze"
                description="Automatically unlock Puryfi when unfreezing"
                checked={config.unlock_on_unfreeze}
                onChange={() => handleToggle("unlock_on_unfreeze")}
                baseColor="emerald"
            />
        </div>
    );
}
