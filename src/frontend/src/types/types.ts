export type MessageRole = 'User' | 'Agent';
export type AskResult = { ok: true; text: string; conversationId: string } | { ok: false; error: string };

export interface Message {
  id: string;
  message: string;
  role: MessageRole;
  createdAt: string;
}

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}
