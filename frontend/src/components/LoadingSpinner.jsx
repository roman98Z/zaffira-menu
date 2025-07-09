import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-amber-50 to-orange-50">
      <div className="text-center">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-amber-200 border-t-amber-600 rounded-full animate-spin mx-auto mb-4"></div>
          <div className="absolute inset-0 w-16 h-16 border-4 border-transparent border-b-amber-400 rounded-full animate-spin mx-auto" 
               style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
        </div>
        
        <h2 className="text-2xl font-bold text-amber-800 mb-2">Caricamento Menù</h2>
        <p className="text-amber-700">Preparando le nostre specialità...</p>
        
        <div className="mt-6 flex items-center justify-center space-x-2">
          <div className="w-2 h-2 bg-amber-500 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-amber-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-amber-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;