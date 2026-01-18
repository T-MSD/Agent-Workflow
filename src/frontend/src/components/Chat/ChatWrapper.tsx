import './Chat.css';
import ChatInputArea from './ChatInputArea';

function ChatWrapper() {
  return (
    <>
      <div className="flex flex-1 w-full h-full rounded-sm text-white bg-neutral-800">
        <ChatInputArea />
      </div>
    </>
  );
};

export default ChatWrapper;