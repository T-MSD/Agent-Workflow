import type { Conversation, Message } from '../types/types';

const API_URL = import.meta.env.VITE_API_URL;

const ROLE_MAP: Record<string, 'User' | 'Agent'> = {
  human: 'User',
  ai: 'Agent',
};

export const invokeAgent = async (
  prompt: string,
  conversationId?: string
): Promise<{ response: string; conversationId: string }> => {
  const response = await fetch(`${API_URL}/invoke`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt,
      conversation_id: conversationId ?? null,
    }),
  });
  if (!response.ok) {
    throw new Error('Failed to get a response from the agent.');
  }
  const data = await response.json();
  return { response: data.response, conversationId: data.conversation_id };
};

export const fetchConversations = async (): Promise<Conversation[]> => {
  const response = await fetch(`${API_URL}/conversations`);
  if (!response.ok) throw new Error('Failed to fetch conversations.');
  return response.json();
};

export const fetchMessages = async (conversationId: string): Promise<Message[]> => {
  const response = await fetch(`${API_URL}/conversations/${conversationId}/messages`);
  if (!response.ok) throw new Error('Failed to fetch messages.');
  const data = await response.json();
  return data.map((msg: { id: string; role: string; content: string; created_at: string }) => ({
    id: msg.id,
    message: msg.content,
    role: ROLE_MAP[msg.role] ?? 'Agent',
    createdAt: msg.created_at,
  }));
};

export const deleteConversation = async (conversationId: string): Promise<void> => {
  const response = await fetch(`${API_URL}/conversations/${conversationId}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete conversation.');
};

export const updateConversationTitle = async (
  conversationId: string,
  title: string
): Promise<Conversation> => {
  const response = await fetch(`${API_URL}/conversations/${conversationId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  if (!response.ok) throw new Error('Failed to update conversation title.');
  return response.json();
};
