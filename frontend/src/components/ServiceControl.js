import React from 'react';
import { startService, stopService } from '../services/api';

function ServiceControl() {
    const handleStart = async () => {
        await startService();
    };

    const handleStop = async () => {
        await stopService();
    };

    return (
        <div>
            <button onClick={handleStart}>Start Suno AI Service</button>
            <button onClick={handleStop}>Stop Suno AI Service</button>
        </div>
    );
}

export default ServiceControl;
