import type { Message, MessageRole} from '../types/messages';

function nowIso(): string {
  return new Date().toISOString();
}

export function createMessage(content: string, role: MessageRole) {
  return {
    id: crypto.randomUUID(),
    message: content,
    role,
    createdAt: nowIso(),

  } as Message;
}
