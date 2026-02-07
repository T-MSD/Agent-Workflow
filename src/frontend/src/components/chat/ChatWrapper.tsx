import './Chat.css';
import ChatInputArea from './ChatInputArea';
import { useEffect, useState } from 'react';
import ChatHistory from './ChatHistory';
import ChatWelcomeHero from './ChatWelcomeHero';
import AlertError from '../ui/AlertError';
import type { Message } from '../../types/types';
import { createMessage } from '@/utils/messages';

function ChatWrapper() {
  const [isFirstMessage, setIsFirstMessage] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [fading, setFading] = useState(false);

  const addMessageToHistory = (content: string, role: 'User' | 'Agent') => {
    setError(null);
    setMessages((prev) => {
      const newMessage: Message = createMessage(content, role);
      return [...prev, newMessage];
    });

    if (isFirstMessage) {
        setIsFirstMessage(false);
    }
  };

  const handleError = (errorMessage: string) => {
    setFading(false);
    setError(errorMessage);
  };

  useEffect(() => {
    if (error === null) return;

    const fadeTimer = setTimeout(() => setFading(true), 2000);
    const removeTimer = setTimeout(() => {
      setError(null);
      setFading(false);
    }, 3000);

    return () => {
      clearTimeout(fadeTimer);
      clearTimeout(removeTimer);
    };
  }, [error]);

  return (
    <>
      <div className={isFirstMessage
        ? "flex flex-col w-full text-white p-6 self-center items-center gap-24"
        : "flex flex-col w-full h-full text-white p-6 bg-neutral-800 items-center rounded-sm gap-8"
      }>
        {isFirstMessage ? <ChatWelcomeHero /> : <ChatHistory messages={messages}/>}
        {error && <AlertError message={error} fading={fading} />}
        <ChatInputArea onSendMessage={addMessageToHistory} onError={handleError} />
      </div>
    </>
  );
};

export default ChatWrapper;
