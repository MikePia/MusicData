import React from 'react';
import CardLayout from './CardLayout';
import OverlayContent from './OverlayContent';
import ImageScroll from './ImageScroll';
import FinalContent from './FinalContent';
import MusicForm from './MusicForm';
import ServiceControl from './ServiceControl';
import '../App.css';

function App() {
  return (
    <div className="App">
      <CardLayout />
      <OverlayContent />
      <ImageScroll />
      <FinalContent>
        <header className="App-header">
          <h1>Music Generator</h1>
        </header>
        <main>
          <ServiceControl />
          <MusicForm />
        </main>
      </FinalContent>
    </div>
  );
}

export default App;
