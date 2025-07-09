import React from 'react';
import { Separator } from './ui/separator';

const MenuHeader = () => {
  return (
    <div className="relative bg-gradient-to-br from-amber-50 to-orange-50 py-12 px-4">
      <div className="max-w-4xl mx-auto text-center">
        <div className="mb-6">
          <h1 className="text-5xl md:text-6xl font-bold text-amber-900 mb-2 tracking-tight">
            Menù 9<span className="text-amber-700">nove</span>
          </h1>
          <div className="w-24 h-1 bg-gradient-to-r from-amber-600 to-orange-600 mx-auto mb-4"></div>
        </div>
        
        <p className="text-xl text-amber-800 font-medium mb-2">
          Scopri le nostre proposte
        </p>
        <p className="text-lg text-amber-700 max-w-2xl mx-auto leading-relaxed">
          per un aperitivo indimenticabile
        </p>
        
        <div className="mt-8 flex items-center justify-center space-x-4 text-amber-600">
          <div className="w-12 h-px bg-amber-400"></div>
          <span className="text-2xl">🍷</span>
          <div className="w-12 h-px bg-amber-400"></div>
        </div>
      </div>
    </div>
  );
};

export default MenuHeader;