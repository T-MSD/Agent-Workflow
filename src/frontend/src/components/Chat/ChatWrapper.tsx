import './Chat.css';
import ChatInputArea from './ChatInputArea';
import { useState } from 'react';
import ChatHistory from './ChatHistory';
import ChatWelcomeHero from './ChatWelcomeHero';

function ChatWrapper() {
  const [isFirstMessage, setIsFirstMessage] = useState(true);

  return (
    <>
      <div className={isFirstMessage
        ? "flex flex-col w-full text-white p-4 self-center items-center gap-24"
        : "flex flex-col w-full h-full text-white p-4 bg-neutral-800 items-center rounded-sm gap-8"
      }>
        {isFirstMessage ? <ChatWelcomeHero /> : <ChatHistory />}
        <ChatInputArea setIsFirstMessage={setIsFirstMessage} />
      </div>
    </>
  );
};

export default ChatWrapper;