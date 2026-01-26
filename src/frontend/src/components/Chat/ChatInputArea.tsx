import './Chat.css';
import { useRef, useState } from 'react'
import { useAgent } from '../../hooks/useAgent';
import ChatSendButton from './ChatSendButton';

interface ChatInputAreaProps {
    onSendMessage: (content: string) => void;
}


function ChatInputArea({onSendMessage }: ChatInputAreaProps) {
    const [prompt, setPrompt] = useState('');
    const { data, isLoading, error, askAgent } = useAgent();
    const inputRef = useRef<HTMLDivElement>(null);
    
    const handleInput = (e: React.ChangeEvent<HTMLDivElement>) => {
        setPrompt(e.currentTarget.innerText);
    };

    const handleSend = () => {
        if (!prompt.trim() || isLoading) return;
        
        askAgent(prompt);
        onSendMessage(prompt);
        
        setPrompt('');
        if (inputRef.current) {
            inputRef.current.innerText = '';
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <>
            {error && <div className="error">{error}</div>}
            
            {data && (
            <div className="response">
                <h3>Result:</h3>
                <p>{data}</p>
            </div>
            )}

            <div className="flex w-full min-h-[48px] p-2 justify-between items-center gap-2 bg-neutral-600 rounded-lg text-white relative">
                {prompt.length === 0 && (
                    <div className="absolute left-3 text-neutral-400 pointer-events-none">
                        Type your message here...
                    </div>
                )}

                <div
                    ref={inputRef}
                    contentEditable={!isLoading}
                    role="textbox"
                    className="flex-1 outline-none overflow-y-auto max-h-60 p-1 break-words whitespace-pre-wrap"
                    onInput={handleInput}
                    onKeyDown={handleKeyDown}
                />
                <ChatSendButton onClick={handleSend} disabled={isLoading || !prompt.trim()} isLoading={isLoading}/>
            </div>
        </>
    );
};

export default ChatInputArea;