export type MessageRole = 'User' | 'Agent';
export type AskResult = { ok: true; text: string } | { ok: false; error: string };

export interface Message {
  id: string;
  message: string;
  role: MessageRole;
  createdAt: string;
}
