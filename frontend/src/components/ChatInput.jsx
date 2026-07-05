import { useState } from "react";

function ChatInput({
  onSubmit,
  disabled,
}) {
  const [value, setValue] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const message = value.trim();

    if (!message || disabled) {
      return;
    }

    const sent = await onSubmit(message);

    if (sent) {
      setValue("");
    }
  }

  function handleKeyDown(event) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      event.currentTarget.form?.requestSubmit();
    }
  }

  return (
    <form
      className="chat-input"
      onSubmit={handleSubmit}
    >
      <textarea
        value={value}
        onChange={(event) =>
          setValue(event.target.value)
        }
        onKeyDown={handleKeyDown}
        placeholder="Message the multi-agent system..."
        rows={1}
        disabled={disabled}
      />

      <button
        type="submit"
        disabled={disabled || !value.trim()}
      >
        Send
      </button>
    </form>
  );
}

export default ChatInput;