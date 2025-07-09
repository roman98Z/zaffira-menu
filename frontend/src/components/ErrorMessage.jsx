import React from 'react';
import { Button } from './ui/button';
import { Alert, AlertDescription } from './ui/alert';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-orange-50 p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-6">
          <div className="text-6xl mb-4">😔</div>
          <h2 className="text-2xl font-bold text-red-800 mb-2">Oops! Qualcosa è andato storto</h2>
        </div>
        
        <Alert className="mb-6 border-red-200 bg-red-50">
          <AlertDescription className="text-red-700">
            {message || 'Si è verificato un errore durante il caricamento del menù.'}
          </AlertDescription>
        </Alert>
        
        <div className="text-center space-y-4">
          <Button 
            onClick={onRetry}
            className="bg-amber-600 hover:bg-amber-700 text-white px-6 py-2"
          >
            Riprova
          </Button>
          
          <p className="text-sm text-gray-600">
            Se il problema persiste, ricarica la pagina o contatta il supporto.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;