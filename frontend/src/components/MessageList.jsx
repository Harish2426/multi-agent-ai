import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";

function MessageList({
  messages,
  isLoading,
  isHistoryLoading,
}) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isLoading]);

  if (isHistoryLoading) {
    return (
      <section className="message-list message-list--center">
        Loading conversation history...
      </section>
    );
  }

  if (!messages.length) {
    return (
      <section className="message-list message-list--center">
        <div className="empty-state">
          <h2>How can the agents help?</h2>

          <p>
            Ask for research, planning, code generation,
            code review, or calculations.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="message-list">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
        />
      ))}

      {isLoading && (
        <article className="message message--assistant">
          <div className="message__role">
            Assistant
          </div>

          <div className="message__content">
            Agents are working...
          </div>
        </article>
      )}

      <div ref={endRef} />
    </section>
  );
}

export default MessageList;