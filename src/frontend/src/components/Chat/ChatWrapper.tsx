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

  const handleSendMessage = (content: string) => {
    const newUserMessage: Message = {
      id: (messages.length + 1).toString(),
      message: content,
      role: 'user',
    };

    setMessages((prev) => [...prev, newUserMessage]);
    
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
        <ChatInputArea onSendMessage={handleSendMessage} />
      </div>
    </>
  );
};

export default ChatWrapper;
