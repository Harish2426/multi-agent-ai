import ChatInput from "./ChatInput";
import MessageList from "./MessageList";

function ChatWindow({
  messages,
  error,
  isLoading,
  isHistoryLoading,
  onSubmit,
}) {
  return (
    <main className="chat-window">
      <header className="chat-header">
        <div>
          <h1>Agent Chat</h1>

          <p>
            Planner · Researcher · Coder · Reviewer ·
            Calculator
          </p>
        </div>
      </header>

      {error && (
        <div
          className="error-banner"
          role="alert"
        >
          {error}
        </div>
      )}

      <MessageList
        messages={messages}
        isLoading={isLoading}
        isHistoryLoading={isHistoryLoading}
      />

      <footer className="chat-footer">
        <ChatInput
          onSubmit={onSubmit}
          disabled={isLoading || isHistoryLoading}
        />

        <p className="chat-footer__hint">
          Enter to send · Shift + Enter for a new line
        </p>
      </footer>
    </main>
  );
}

export default ChatWindow;