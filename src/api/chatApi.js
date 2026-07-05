import apiClient from "./client";

export async function getHealth() {
  const response = await apiClient.get("/health");
  return response.data;
}

export async function sendMessage({
  message,
  conversationId,
}) {
  const response = await apiClient.post("/chat", {
    message,
    conversation_id: conversationId || null,
  });

  return response.data;
}

export async function getConversationHistory(conversationId) {
  const response = await apiClient.get(
    `/conversations/${encodeURIComponent(conversationId)}/history`
  );

  return response.data;
}

export async function deleteConversation(conversationId) {
  const response = await apiClient.delete(
    `/conversations/${encodeURIComponent(conversationId)}`
  );

  return response.data;
}