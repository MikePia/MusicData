import React, { useState } from 'react';
import { startService, stopService } from '../services/api';

function ServiceControl() {
    console.log("ServiceControl function defining stuff");
    const [statusMessage, setStatusMessage] = useState('');

    const handleStart = async () => {
        console.log("Starting service from ServiceControl");
        const result = await startService();
        setStatusMessage(result.message || "Service started");
    };

    const handleStop = async () => {
        console.log("Stopping service from ServiceControl");
        const result = await stopService();
        console.log("Stop Service Result:", result);
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
