import React, { useEffect, useState } from 'react';
import '../App.css'

const images = ['/path/to/image1.jpg', '/path/to/image2.jpg', '/path/to/image3.jpg'];

const ImageScroll = () => {
  const [currentImage, setCurrentImage] = useState(0);

  const handleScroll = () => {
    const scrollPosition = window.scrollY;
    const imageIndex = Math.floor(scrollPosition / window.innerHeight) % images.length;
    setCurrentImage(imageIndex);
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div className="image-scroll">
      <img src={images[currentImage]} alt="Scroll Image" />
    </div>
  );
};

export default ImageScroll;
