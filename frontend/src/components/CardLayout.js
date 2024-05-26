import React from 'react';
import { motion } from 'framer-motion';
import '../App.css'


const CardLayout = () => {
  return (
    <div className="card-grid">
      <motion.div className="card" animate={{ opacity: 1 }} initial={{ opacity: 0 }} transition={{ duration: 1 }}>
        {/* Hamburger Menu */}
      </motion.div>
      <motion.div className="card card1">Animated Content</motion.div>
      <motion.div className="card card2">Animated Content</motion.div>
      <motion.div className="card card3">Static Content</motion.div>
      <motion.div className="card card4">Animated Content</motion.div>
      <motion.div className="card card5">Animated Content</motion.div>
      <motion.div className="card card6">Animated Content</motion.div>
    </div>
  );
};

export default CardLayout;
