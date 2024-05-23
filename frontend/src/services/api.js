import config from '../config';

export const generateMusic = async (prompt) => {
    const response = await fetch(`${config.apiBaseUrl}/api/generate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });
    const data = await response.json();
    console.log('Generate Music Response:', data);
    return data;
};

export const startService = async () => {
    const response = await fetch(`${config.apiBaseUrl}/api/start_service`, {
        method: 'POST',
    });
    console.log('Start Service Full Response:', response);
    if (response.ok) {
        const data = await response.json();
        console.log('Start Service Response:', data);
        return data;
    } else {
        const error = await response.json();
        console.log('Start Service Error:', error);
        return { status: "error", message: error.detail || "Failed to start service" };
    }
};

export const stopService = async () => {
    const response = await fetch(`${config.apiBaseUrl}/api/stop_service`, {
        method: 'POST',
    });
    console.log('Stop Service Full Response:', response);
    if (response.ok) {
        const data = await response.json();
        console.log('Stop Service Response:', data);
        return data;
    } else {
        const error = await response.json();
        console.log('Stop Service Error:', error);
        return { status: "error", message: error.detail || "Failed to stop service" };
    }
};
