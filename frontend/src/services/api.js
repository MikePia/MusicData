export const generateMusic = async (prompt) => {
    const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });
    return response.json();
};

export const startService = async () => {
    const response = await fetch('/api/start_service', {
        method: 'POST',
    });
    if (response.ok) {
        return response.json();
    } else {
        const error = await response.json();
        return { status: "error", message: error.detail || "Failed to start service" };
    }
};

export const stopService = async () => {
    const response = await fetch('/api/stop_service', {
        method: 'POST',
    });
    if (response.ok) {
        return response.json();
    } else {
        const error = await response.json();
        return { status: "error", message: error.detail || "Failed to stop service" };
    }
};
