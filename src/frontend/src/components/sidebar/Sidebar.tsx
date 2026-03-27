import { Plus } from 'lucide-react';
import type { Conversation } from '../../types/types';
import ConversationItem from './ConversationItem';

interface SidebarProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewConversation: () => void;
  onDeleteConversation: (id: string) => void;
}

function Sidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
}: SidebarProps) {
  return (
    <div className="flex flex-col w-64 h-full bg-neutral-900 border-r border-neutral-700 p-3 gap-3">
      <button
        onClick={onNewConversation}
        className="flex items-center gap-2 w-full px-3 py-2 rounded-md text-sm text-white bg-neutral-700 hover:bg-neutral-600 transition-colors cursor-pointer"
      >
        <Plus size={16} />
        New Chat
      </button>

      <div className="flex flex-col gap-1 overflow-y-auto flex-1">
        {conversations.map((conversation) => (
          <ConversationItem
            key={conversation.id}
            conversation={conversation}
            isActive={conversation.id === activeConversationId}
            onSelect={onSelectConversation}
            onDelete={onDeleteConversation}
          />
        ))}
      </div>
    </div>
  );
}

export default Sidebar;
