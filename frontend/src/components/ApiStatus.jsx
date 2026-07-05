import { useEffect, useState } from "react";

import { getHealth } from "../../../src/api/chatApi";

function ApiStatus() {
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    let active = true;

    async function checkHealth() {
      try {
        const result = await getHealth();

        if (active) {
          setStatus(
            result.status === "ok"
              ? "online"
              : "unavailable"
          );
        }
      } catch {
        if (active) {
          setStatus("offline");
        }
      }
    }

    checkHealth();

    const timer = window.setInterval(
      checkHealth,
      30000
    );

    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, []);

  return (
    <div className={`api-status api-status--${status}`}>
      <span className="api-status__dot" />

      <span>
        {status === "online"
          ? "API online"
          : status === "checking"
            ? "Checking API"
            : "API unavailable"}
      </span>
    </div>
  );
}

export default ApiStatus;