import type { Message } from '../../types/types';
import ChatIcon from './ChatIcon';

function ChatMessage({ message, role, }: Message) {
    return (
        <div className='flex flex-col w-full'>
            <ChatIcon role={role}/>
            <div className={ role === 'User'
                ? "ml-auto bg-neutral-600 p-3 rounded-lg text-white max-w-[60%] break-words whitespace-pre-wrap"
                : "content-start p-3 text-white"
            }>
                {message}
            </div>
        </div>
    );
}

export default ChatMessage;
