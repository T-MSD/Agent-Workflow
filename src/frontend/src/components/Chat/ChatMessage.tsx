interface ChatMessageProps {
    id: string;
    message: string;
    role: 'user' | 'agent';
}

function ChatMessage({ id, message, role }: ChatMessageProps) {
    return (
        <div className="flex self-end bg-neutral-600 p-3 rounded-lg text-white">ID: {id} - Chat {role} Message: {message}</div>
    );
}

export default ChatMessage;