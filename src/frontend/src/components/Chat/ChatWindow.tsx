import { useState } from 'react'
import { useAgent } from '../../hooks/useAgent';

function ChatWindow() {
  const [prompt, setPrompt] = useState('');
  const { data, isLoading, error, askAgent } = useAgent();

  const handleSend = () => {
    askAgent(prompt);
};

  return (
    <>
      <div className="container">
        <textarea 
          value={prompt} 
          onChange={(e) => setPrompt(e.target.value)}
          disabled={isLoading}
        />
      </div>
      <div>
        <button onClick={handleSend} disabled={isLoading || !prompt}>
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
}

export default ChatWindow;
