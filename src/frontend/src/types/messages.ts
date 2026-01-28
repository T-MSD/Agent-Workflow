export type MessageRole = 'User' | 'Agent';

export interface Message {
  id: string;
  message: string;
  role: MessageRole;
  createdAt: string;
}
