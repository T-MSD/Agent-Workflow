import './Chat.css';
import ChatInputArea from './ChatInputArea';

function ChatWindow() {
  return (
    <>
      <div className="flex flex-1 w-full h-full bg-gray-300 rounded-sm">
        <ChatInputArea />
      </div>
    </>
  );
};

export default ChatWindow;