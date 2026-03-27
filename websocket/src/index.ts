import * as SDK from "@pury-fi/plugin-sdk/websocket";

const server = new SDK.WebSocketServer(8093);
server.setDebug(true);

server.on("connection", (connection) => {
   connection.on("open", async () => {
      await new Promise<void>((resolve) => {
         connection.on("message", "ready", (payload) => {
            const res = connection.handleReadyMessage(payload);
            if (res.type === "ok") {
               resolve();
            }
            return res;
         });
      });

      let manifest: SDK.PluginManifest = {
         name: "Plune Watcher",
         version: "1.0.0",
         description: "Logs media scan and trigger consequences",
         author: "Sereti <httxsereti@gmail.com>",
         website: null,
      };
      await connection
         .sendMessage("setPluginManifest", { manifest })
         .then((res) => {
            if (res.type === "error") {
               throw new Error(`Failed to set plugin manifest: ${res.message}`);
            }
         });

      let configuration: SDK.PluginConfiguration = {
         logEmptyObjects: {
            name: "Log Empty Scans",
            type: "boolean",
            value: false,
         },
         chasterToken: {
            name: "Your Chaster API token",
            type: "string",
            value: "",
         },
      };
      await connection
         .sendMessage("setPluginConfiguration", { configuration })
         .then((res) => {
            if (res.type === "error") {
               throw new Error(
                  `Failed to set plugin configuration: ${res.message}`
               );
            }
         });

      connection.on("message", "configurationChange", (payload) => {
         configuration = payload.configuration;
      });

      const intents: SDK.PluginIntent[] = ["readMediaProcesses"];

      const { intents: grantedIntents } = await connection
         .sendMessage("getPluginIntents", {})
         .then((res) => {
            if (res.type === "error") {
               throw new Error(`Failed to get plugin intents: ${res.message}`);
            }
            return res;
         });

      if (!intents.every((intent) => grantedIntents.includes(intent))) {
         await connection
            .sendMessage("requestPluginIntents", { intents })
            .then((res) => {
               if (res.type === "error") {
                  throw new Error(
                     `Failed to request plugin intents: ${res.message}`
                  );
               }
            });

         await new Promise<void>((resolve) => {
            connection.on(
               "message",
               "intentsGrant",
               function listener({ intents: grantedIntents }) {
                  if (
                     intents.every((intent) => grantedIntents.includes(intent))
                  ) {
                     connection.off("message", "intentsGrant", listener);
                     resolve();
                  }
               }
            );
         });
      }

      await connection
         .sendMessage("subscribeToStaticMediaScans", {})
         .then((res) => {
            if (res.type === "error") {
               throw new Error(
                  `Failed to subscribe to static media scans: ${res.message}`
               );
            }
         });

      connection.on("message", "staticMediaScan", ({ objects }) => {
         const isLogEmpty = Boolean(configuration.logEmptyObjects?.value);
         if (!isLogEmpty && objects.length === 0) return;
         console.log(`Scan event: ${objects.length} object(s) detected`);
         for (const obj of objects) {
            const label = SDK.Label[obj.label]
            
            console.log(
               `label=${label} score=${obj.score.toFixed(3)} at (${obj.rect.x.toFixed(3)}, ${obj.rect.y.toFixed(3)}) ${obj.rect.width.toFixed(3)}x${obj.rect.height.toFixed(3)}`
            );
         }
      });
   });
});
