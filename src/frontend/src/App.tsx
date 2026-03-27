import './App.css'
import ChatWrapper from './components/chat/ChatWrapper';
import Sidebar from './components/sidebar/Sidebar';
import { useConversations } from './hooks/useConversations';
import { useState } from 'react';

function App() {
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const {
    conversations,
    removeConversation,
    refreshConversations,
  } = useConversations();

  const handleSelectConversation = (id: string) => {
    setCurrentConversationId(id);
  };

  const handleNewChat = () => {
    setCurrentConversationId(null);
  };

  const handleDeleteConversation = async (id: string) => {
    const deleted = await removeConversation(id);
    if (deleted && currentConversationId === id) {
      setCurrentConversationId(null);
    }
  };

  const handleNewConversation = (conversationId: string) => {
    setCurrentConversationId(conversationId);
    refreshConversations();
  };

  return (
    <>
      <div className="flex w-screen h-dvh bg-neutral-900 p-4 gap-4">
        <Sidebar
          conversations={conversations}
          activeConversationId={currentConversationId}
          onSelectConversation={handleSelectConversation}
          onNewConversation={handleNewChat}
          onDeleteConversation={handleDeleteConversation}
        />
        <ChatWrapper
          conversationId={currentConversationId}
          onNewConversation={handleNewConversation}
        />
      </div>
    </>
  );
}

export default App;
