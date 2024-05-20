import React from 'react';
import MusicForm from './MusicForm';
import ServiceControl from './ServiceControl';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Music Generator</h1>
            </header>
            <main>
                <ServiceControl />
                <MusicForm />
            </main>
        </div>
    );
}

export default App;
