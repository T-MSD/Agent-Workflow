import ChatMessage from "./ChatMessage";

interface Message {
    id: string;
    message: string;
    role: 'user' | 'agent';
}

function ChatHistory({ messages }: { messages: Message[] }) {

    return (
        <div className="flex flex-col w-full h-full bg-red-300">
            {messages.map((msg, index) => (
                <ChatMessage key={index} id={msg.id} message={msg.message} role={msg.role} />
            ))}
        </div>
    )
}

export default ChatHistory;