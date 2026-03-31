import { useState, useEffect } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface Log {
  id: number;
  title: string;
  content: string;
}

function App() {
  const [logs, setLogs] = useState<Log[]>([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [health, setHealth] = useState('Checking...');
  const [file, setFile] = useState<File | null>(null);

  useEffect(() => {
    checkHealth();
    fetchLogs();
  }, []);

  const checkHealth = async () => {
    try {
      const res = await fetch(`${API_URL}/health`);
      const data = await res.json();
      setHealth(data.status);
    } catch (e) {
      setHealth('Error connecting to backend');
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await fetch(`${API_URL}/logs`);
      const data = await res.json();
      setLogs(data);
    } catch (e) {
      console.error('Failed to fetch logs', e);
    }
  };

  const createLog = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await fetch(`${API_URL}/logs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content }),
      });
      setTitle('');
      setContent('');
      fetchLogs();
    } catch (e) {
      console.error('Failed to create log', e);
    }
  };

  const deleteLog = async (id: number) => {
    try {
      await fetch(`${API_URL}/logs/${id}`, { method: 'DELETE' });
      fetchLogs();
    } catch (e) {
      console.error('Failed to delete log', e);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      alert(`File uploaded! Saved path: ${data.saved_path}`);
      setFile(null);
    } catch (e) {
      console.error('Failed to upload', e);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Infra-Learning Journal</h1>
      <p>Backend Status: <strong style={{ color: health === 'ok' ? 'green' : 'red' }}>{health}</strong></p>

      <section style={{ marginBottom: '40px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
        <h2>Create Log</h2>
        <form onSubmit={createLog} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <input 
            placeholder="Title" 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            required 
            style={{ padding: '8px', fontSize: '16px' }}
          />
          <textarea 
            placeholder="Content" 
            value={content} 
            onChange={(e) => setContent(e.target.value)} 
            required 
            rows={4}
            style={{ padding: '8px', fontSize: '16px' }}
          />
          <button type="submit" style={{ padding: '10px', fontSize: '16px', cursor: 'pointer', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>Add Log</button>
        </form>
      </section>

      <section style={{ marginBottom: '40px' }}>
        <h2>Logs</h2>
        {logs.length === 0 ? <p>No logs found. Add one above!</p> : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {logs.map(log => (
              <li key={log.id} style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '15px', borderRadius: '8px' }}>
                <h3 style={{ marginTop: 0 }}>{log.title}</h3>
                <p style={{ whiteSpace: 'pre-wrap' }}>{log.content}</p>
                <button 
                  onClick={() => deleteLog(log.id)}
                  style={{ padding: '5px 10px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section style={{ padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
        <h2>File Upload Test</h2>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <button 
            onClick={handleUpload} 
            disabled={!file}
            style={{ padding: '8px 15px', cursor: file ? 'pointer' : 'not-allowed', backgroundColor: file ? '#28a745' : '#ccc', color: 'white', border: 'none', borderRadius: '4px' }}
          >
            Upload File
          </button>
        </div>
      </section>
    </div>
  );
}

export default App;
