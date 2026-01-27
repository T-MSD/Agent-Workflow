export type MessageRole = 'user' | 'agent';

export interface Message {
  id: string;
  message: string;
  role: MessageRole;
  createdAt: string;
}
