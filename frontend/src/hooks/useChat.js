import { useCallback, useEffect, useState } from "react";

import {
  deleteConversation,
  getConversationHistory,
  sendMessage,
} from "../../../src/api/chatApi";

const STORAGE_KEY = "multi-agent-ai-conversation-id";

export function useChat() {
  const [conversationId, setConversationId] = useState(
    () => localStorage.getItem(STORAGE_KEY)
  );

  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isHistoryLoading, setIsHistoryLoading] =
    useState(false);
  const [error, setError] = useState("");

  const loadHistory = useCallback(async (id) => {
    if (!id) {
      setMessages([]);
      return;
    }

    setIsHistoryLoading(true);
    setError("");

    try {
      const result = await getConversationHistory(id);

      setMessages(result.history || []);
    } catch (requestError) {
      console.error(
        "Failed to load conversation history:",
        requestError
      );

      setError("Unable to load conversation history.");
    } finally {
      setIsHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    if (conversationId) {
      loadHistory(conversationId);
    }
  }, [conversationId, loadHistory]);

  async function submitMessage(message) {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || isLoading) {
      return false;
    }

    setError("");
    setIsLoading(true);

    const temporaryUserMessage = {
      id: `temporary-user-${Date.now()}`,
      role: "user",
      content: trimmedMessage,
      timestamp: new Date().toISOString(),
      sequence: Number.MAX_SAFE_INTEGER - 1,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      temporaryUserMessage,
    ]);

    try {
      const result = await sendMessage({
        message: trimmedMessage,
        conversationId,
      });

      const resolvedConversationId =
        result.conversation_id;

      if (resolvedConversationId !== conversationId) {
        localStorage.setItem(
          STORAGE_KEY,
          resolvedConversationId
        );

        setConversationId(resolvedConversationId);
      }

      await loadHistory(resolvedConversationId);

      return true;
    } catch (requestError) {
      console.error("Chat request failed:", requestError);

      setMessages((currentMessages) =>
        currentMessages.filter(
          (item) => item.id !== temporaryUserMessage.id
        )
      );

      const detail =
        requestError.response?.data?.detail;

      setError(
        typeof detail === "string"
          ? detail
          : "Unable to send the message."
      );

      return false;
    } finally {
      setIsLoading(false);
    }
  }

  function startNewChat() {
    localStorage.removeItem(STORAGE_KEY);
    setConversationId(null);
    setMessages([]);
    setError("");
  }

  async function removeConversation() {
    if (!conversationId || isLoading) {
      return false;
    }

    setError("");

    try {
      await deleteConversation(conversationId);

      startNewChat();

      return true;
    } catch (requestError) {
      console.error(
        "Failed to delete conversation:",
        requestError
      );

      setError("Unable to delete the conversation.");

      return false;
    }
  }

  return {
    conversationId,
    messages,
    isLoading,
    isHistoryLoading,
    error,
    submitMessage,
    startNewChat,
    removeConversation,
    reloadHistory: () => loadHistory(conversationId),
  };
}