import React, { useState } from 'react';
import { initializeDatabase } from '../utils/initializeDatabase';

export function AdminPanel() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');

  const handleInitialize = async () => {
    setLoading(true);
    setStatus('Initializing database...');
    
    try {
      const success = await initializeDatabase();
      setStatus(success ? 'Database initialized successfully!' : 'Failed to initialize database');
    } catch (error) {
      setStatus('Error initializing database');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 p-4 bg-white rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold mb-2">Admin Panel</h3>
      <button
        onClick={handleInitialize}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
      >
        {loading ? 'Initializing...' : 'Initialize Database'}
      </button>
      {status && (
        <p className="mt-2 text-sm text-gray-600">{status}</p>
      )}
    </div>
  );
}