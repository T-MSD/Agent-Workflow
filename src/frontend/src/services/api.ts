const API_URL = import.meta.env.VITE_API_URL;

export const invokeAgent = async (prompt: string): Promise<string> => {
    const response = await fetch(`${API_URL}/invoke`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
    });
    if (!response.ok) {
    throw new Error('Failed to get a response from the agent.');
    }
    const data = await response.json();
    return data.output;
};