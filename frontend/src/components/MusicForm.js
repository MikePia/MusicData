import React, { useState } from 'react';
import { generateMusic } from '../services/api';

function MusicForm() {
    const [prompt, setPrompt] = useState('');
    const [musicUrl, setMusicUrl] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await generateMusic(prompt);
        setMusicUrl(response.music_url);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text" 
                value={prompt} 
                onChange={(e) => setPrompt(e.target.value)} 
                placeholder="Enter your music prompt"
            />
            <button type="submit">Generate Music</button>
            {musicUrl && <audio controls src={musicUrl}></audio>}
        </form>
    );
}

export default MusicForm;
