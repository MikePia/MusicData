import React, { useState } from 'react';
import '../App.css'

const OverlayContent = () => {
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <div className="overlay-content">
      <div className="section">
        <div className="hamburger-menu">Menu</div>
      </div>
      <div className="section">
        <div className="video-container">
          <video src="/path/to/video.mp4" controls={isPlaying}></video>
          <div 
            className="play-button" 
            onMouseEnter={() => setIsPlaying(true)} 
            onMouseLeave={() => setIsPlaying(false)}
          >
            Play
          </div>
        </div>
      </div>
      <div className="section transparent-section">Transparent Content</div>
    </div>
  );
};

export default OverlayContent;
