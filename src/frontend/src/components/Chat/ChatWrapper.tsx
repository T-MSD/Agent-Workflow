import './Chat.css';
import ChatInputArea from './ChatInputArea';
import { useState } from 'react';
import ChatHistory from './ChatHistory';
import ChatWelcomeHero from './ChatWelcomeHero';

interface Message {
  id: string;
  message: string;
  role: 'user' | 'agent';
}

function ChatWrapper() {
  const [isFirstMessage, setIsFirstMessage] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);

  const addMessageToHistory = (content: string, role: 'user' | 'agent') => {
    setMessages((prev) => {
      const newMessage: Message = {
        id: (prev.length + 1).toString(),
        message: content,
        role: role,
      };
      return [...prev, newMessage];
    });

    if (isFirstMessage) {
        setIsFirstMessage(false);
    }
  };

  return (
    <>
      <div className={isFirstMessage
        ? "flex flex-col w-full text-white p-4 self-center items-center gap-24"
        : "flex flex-col w-full h-full text-white p-4 bg-neutral-800 items-center rounded-sm gap-8"
      }>
        {isFirstMessage ? <ChatWelcomeHero /> : <ChatHistory messages={messages}/>}
        <ChatInputArea onSendMessage={addMessageToHistory} />
      </div>
    </>
  );
};

export default ChatWrapper;
