import { Trash2, MessageSquare } from 'lucide-react';
import type { Conversation } from '../../types/types';

interface ConversationItemProps {
  conversation: Conversation;
  isActive: boolean;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}

function ConversationItem({ conversation, isActive, onSelect, onDelete }: ConversationItemProps) {
  return (
    <div
      onClick={() => onSelect(conversation.id)}
      className={`group flex items-center gap-2 px-3 py-2 rounded-md cursor-pointer transition-colors ${
        isActive
          ? 'bg-neutral-700 text-white'
          : 'text-neutral-300 hover:bg-neutral-800 hover:text-white'
      }`}
    >
      <MessageSquare size={16} className="shrink-0 text-neutral-400" />
      <span className="truncate text-sm flex-1">{conversation.title}</span>
      <button
        onClick={(e) => {
          e.stopPropagation();
          onDelete(conversation.id);
        }}
        className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-neutral-600 transition-opacity text-neutral-400 hover:text-red-400"
      >
        <Trash2 size={14} />
      </button>
    </div>
  );
}

export default ConversationItem;
