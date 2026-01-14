import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { invokeAgent } from './services/api'

function App() {
  const [count, setCount] = useState(0)

  const [prompt, setPrompt] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const handleSubmit = async () => {
  if (!prompt) {
    setError('Please enter a prompt.');
    return;
  }
  setIsLoading(true);
  setError(null);
  setResponse('');
  try {
    const result = await invokeAgent(prompt);
    setResponse(result);
  } catch (err) {
    setError('Failed to get a response from the agent. Please try again.');
    console.error(err); // For debugging
  } finally {
    setIsLoading(false);
  }
};

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
       <h1>Agent Interaction</h1>
      <div className="card">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt here"
          disabled={isLoading}
          style={{ width: '80%', marginBottom: '10px' }}
        />
        <button onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? 'Loading...' : 'Invoke Agent'}
        </button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        
        {response && (
          <div style={{ marginTop: '20px', textAlign: 'left' }}>
            <h3>Agent Response:</h3>
            <p>{response}</p>
          </div>
        )}
      </div>
    </>
  )
}

export default App
