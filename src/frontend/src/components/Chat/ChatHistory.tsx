import ChatMessage from "./ChatMessage";
import type { Message } from '../../types/types';

function ChatHistory({ messages }: { messages: Message[] }) {

    return (
        <div className="flex flex-col w-full h-full gap-4 overflow-y-auto">
            {messages.map((msg) => (
                <ChatMessage key={msg.id} {...msg} />
            ))}
        </div>
    )
}

export default ChatHistory;