import './Chat.css';
import { useState } from 'react'
import { useAgent } from '../../hooks/useAgent';

function ChatInputArea() {
    const [prompt, setPrompt] = useState('');
    const { data, isLoading, error, askAgent } = useAgent();

    const handleSend = () => {
        askAgent(prompt);
    };
    return (
        <>
        <div className="w-full p-4 bg-white rounded-sm">
            <h2 className="text-xl font-bold mb-4">Chat Input Area</h2>
            <textarea 
            className="w-full h-32 p-2 border border-gray-300 rounded-sm" 
            placeholder="Type your message here..."
            value={prompt} 
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isLoading}
            />
            <button 
                onClick={handleSend} 
                disabled={isLoading || !prompt}
                className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-sm">
                {isLoading ? 'Thinking...' : 'Ask AI'}
            </button>

            {error && <div className="error">{error}</div>}
        
            {data && (
            <div className="response">
                <h3>Result:</h3>
                <p>{data}</p>
            </div>
            )}
        </div>
        </>
    );
};

export default ChatInputArea;