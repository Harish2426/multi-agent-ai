function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <article
      className={
        isUser
          ? "message message--user"
          : "message message--assistant"
      }
    >
      <div className="message__role">
        {isUser ? "You" : "Assistant"}
      </div>

      <div className="message__content">
        {message.content}
      </div>
    </article>
  );
}

export default MessageBubble;