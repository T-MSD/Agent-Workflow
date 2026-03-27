import './Chat.css';
import ChatInputArea from './ChatInputArea';
import { useEffect, useState } from 'react';
import ChatHistory from './ChatHistory';
import ChatWelcomeHero from './ChatWelcomeHero';
import AlertError from '../ui/AlertError';
import type { Message } from '../../types/types';
import { createMessage } from '@/utils/messages';
import { fetchMessages } from '../../services/api';

interface ChatWrapperProps {
  conversationId: string | null;
  onNewConversation: (conversationId: string) => void;
}

function ChatWrapper({ conversationId, onNewConversation }: ChatWrapperProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [fading, setFading] = useState(false);

  const isWelcome = !conversationId && messages.length === 0;

  useEffect(() => {
    if (!conversationId) {
      setMessages([]);
      return;
    }

    let cancelled = false;
    fetchMessages(conversationId)
      .then((msgs) => {
        if (!cancelled) setMessages(msgs);
      })
      .catch((err) => {
        console.error('Failed to load messages:', err);
      });

    return () => { cancelled = true; };
  }, [conversationId]);

  const addMessageToHistory = (content: string, role: 'User' | 'Agent') => {
    setError(null);
    setMessages((prev) => {
      const newMessage: Message = createMessage(content, role);
      return [...prev, newMessage];
    });
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
      <div className={isWelcome
        ? "flex flex-col w-full text-white p-6 self-center items-center gap-24"
        : "flex flex-col w-full h-full text-white p-6 bg-neutral-800 items-center rounded-sm gap-8"
      }>
        {isWelcome ? <ChatWelcomeHero /> : <ChatHistory messages={messages}/>}
        {error && <AlertError message={error} fading={fading} />}
        <ChatInputArea
          conversationId={conversationId}
          onSendMessage={addMessageToHistory}
          onNewConversation={onNewConversation}
          onError={handleError}
        />
      </div>
    </>
  );
};

export default ChatWrapper;
