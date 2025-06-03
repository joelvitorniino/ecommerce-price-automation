import { useState, useEffect } from 'react';
import { startAutomation, stopAutomation, getAutomationStatus } from '../../services/api';
import './PriceMonitor.css';

const PriceMonitor: React.FC = () => {
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [isConnected, setIsConnected] = useState<boolean>(true);
  const [lastUpdate, setLastUpdate] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        console.log('Checking automation status at', new Date().toISOString());
        const status = await getAutomationStatus();
        setIsRunning(status.is_running);
        setLastUpdate(status.last_update);
        setIsConnected(true);
        setError(null);
        console.log('Automation status:', status);
      } catch (error) {
        setIsConnected(false);
        setError('Failed to fetch automation status');
        console.error('Status check failed:', error);
      }
    };
    checkStatus();
    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    try {
      console.log('Starting automation');
      await startAutomation();
      setIsRunning(true);
      setError(null);
      console.log('Automation started successfully');
    } catch (error) {
      setIsConnected(false);
      setError('Failed to start automation');
      console.error('Start automation failed:', error);
    }
  };

  const handleStop = async () => {
    try {
      console.log('Stopping automation');
      await stopAutomation();
      setIsRunning(false);
      setError(null);
      console.log('Automation stopped successfully');
    } catch (error) {
      setIsConnected(false);
      setError('Failed to stop automation');
      console.error('Stop automation failed:', error);
    }
  };

  return (
    <div className="price-monitor">
      <div className="status">
        <span className={`status-indicator ${isConnected ? 'online' : 'offline'}`}></span>
        <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
      </div>
      <div className="status">
        <span className={`status-indicator ${isRunning ? 'running' : 'stopped'}`}></span>
        <span>Price Updates: {isRunning ? 'Running' : 'Stopped'}</span>
      </div>
      {lastUpdate && (
        <div className="status">
          <span>Last Update: {new Date(lastUpdate).toLocaleString()}</span>
        </div>
      )}
      {error && (
        <div className="error">
          <span>{error}</span>
        </div>
      )}
      <div className="controls">
        <button onClick={handleStart} disabled={isRunning}>
          Start Updates
        </button>
        <button onClick={handleStop} disabled={!isRunning}>
          Stop Updates
        </button>
      </div>
    </div>
  );
};

export default PriceMonitor;