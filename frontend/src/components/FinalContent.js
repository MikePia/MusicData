import React from 'react';
import '../App.css';

const FinalContent = ({ children }) => {
  return (
    <div className="final-content">
      <div className="mission-statement">
        <p className="transparent-text">Mission Statement</p>
        <p>About the company</p>
      </div>
      {children}
      <div className="services-links">
        <a href="/service1" className="hover-link">Service 1</a>
        <a href="/service2" className="hover-link">Service 2</a>
      </div>
    </div>
  );
};

export default FinalContent;
