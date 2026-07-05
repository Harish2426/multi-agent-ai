import ChatWindow from "./components/ChatWindow";
import Sidebar from "./components/Sidebar";
import { useChat } from "./hooks/useChat";

function App() {
  const {
    conversationId,
    messages,
    isLoading,
    isHistoryLoading,
    error,
    submitMessage,
    startNewChat,
    removeConversation,
  } = useChat();

  return (
    <div className="app-shell">
      <Sidebar
        conversationId={conversationId}
        onNewChat={startNewChat}
        onDelete={removeConversation}
        disabled={isLoading || isHistoryLoading}
      />

      <ChatWindow
        messages={messages}
        error={error}
        isLoading={isLoading}
        isHistoryLoading={isHistoryLoading}
        onSubmit={submitMessage}
      />
    </div>
  );
}

export default App;