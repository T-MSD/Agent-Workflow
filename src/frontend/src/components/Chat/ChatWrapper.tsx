import './Chat.css';
import ChatInputArea from './ChatInputArea';
import { useState } from 'react';
import ChatHistory from './ChatHistory';
import ChatWelcomeHero from './ChatWelcomeHero';
import type { Message } from '../../types/types';
import { createMessage } from '@/utils/messages';

function ChatWrapper() {
  const [isFirstMessage, setIsFirstMessage] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);

  const addMessageToHistory = (content: string, role: 'User' | 'Agent') => {
    setMessages((prev) => {
      const newMessage: Message = createMessage(content, role);
      return [...prev, newMessage];
    });

    if (isFirstMessage) {
        setIsFirstMessage(false);
    }
  };

  return (
    <>
      <div className={isFirstMessage
        ? "flex flex-col w-full text-white p-6 self-center items-center gap-24"
        : "flex flex-col w-full h-full text-white p-6 bg-neutral-800 items-center rounded-sm gap-8"
      }>
        {isFirstMessage ? <ChatWelcomeHero /> : <ChatHistory messages={messages}/>}
        <ChatInputArea onSendMessage={addMessageToHistory} />
      </div>
    </>
  );
};

export default ChatWrapper;
