import React, { useState } from 'react';
import { startService, stopService } from '../services/api';

function ServiceControl() {
    const [statusMessage, setStatusMessage] = useState('');

    const handleStart = async () => {
        const result = await startService();
        setStatusMessage(result.message || "Service started");
    };

    const handleStop = async () => {
        const result = await stopService();
        setStatusMessage(result.message || "Service stopped");
    };

    return (
        <div>
            <button onClick={handleStart}>Start Suno AI Service</button>
            <button onClick={handleStop}>Stop Suno AI Service</button>
            {statusMessage && <p>{statusMessage}</p>}
        </div>
    );
}

export default ServiceControl;
