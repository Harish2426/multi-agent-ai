import { useEffect, useState } from "react";

import { getHealth } from "./api/chatApi";


function App() {
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    async function checkApi() {
      try {
        const result = await getHealth();
        setStatus(result.status);
      } catch (error) {
        console.error("API health check failed:", error);
        setStatus("unavailable");
      }
    }

    checkApi();
  }, []);

  return (
    <main>
      <h1>Multi-Agent AI</h1>

      <p>
        API status: <strong>{status}</strong>
      </p>
    </main>
  );
}


export default App;