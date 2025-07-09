import React from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';

const MenuSection = ({ category, items }) => {
  const categoryConfig = {
    apericena: { 
      title: 'Apericena', 
      icon: '🍢',
      color: 'from-amber-500 to-orange-500',
      bgColor: 'bg-amber-50'
    },
    bevande: { 
      title: 'Bevande', 
      icon: '🥤',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50'
    },
    vini: { 
      title: 'Vini e Bollicine', 
      icon: '🍷',
      color: 'from-purple-500 to-pink-500',
      bgColor: 'bg-purple-50'
    },
    mixology: { 
      title: 'Mixology', 
      icon: '🍸',
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-50'
    },
    gin: { 
      title: 'I Nostri Gin', 
      icon: '🍃',
      color: 'from-teal-500 to-cyan-500',
      bgColor: 'bg-teal-50'
    }
  };

  const config = categoryConfig[category];
  
  return (
    <div id={category} className={`py-16 ${config.bgColor}`}>
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center space-x-4 mb-4">
            <div className="w-16 h-px bg-gradient-to-r from-transparent via-current to-transparent opacity-30"></div>
            <span className="text-4xl">{config.icon}</span>
            <div className="w-16 h-px bg-gradient-to-r from-transparent via-current to-transparent opacity-30"></div>
          </div>
          <h2 className={`text-4xl md:text-5xl font-bold bg-gradient-to-r ${config.color} bg-clip-text text-transparent mb-2`}>
            {config.title}
          </h2>
          <div className={`w-20 h-1 bg-gradient-to-r ${config.color} mx-auto rounded-full`}></div>
        </div>
        
        <div className="grid gap-6 md:grid-cols-2">
          {items.map((item) => (
            <Card key={item.id} className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg hover:transform hover:scale-105">
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-xl font-bold text-gray-800 group-hover:text-amber-700 transition-colors">
                    {item.name}
                  </h3>
                  <Badge variant="secondary" className="ml-4 text-lg font-bold text-amber-700 bg-amber-100 shrink-0">
                    €{item.price.toFixed(2)}
                  </Badge>
                </div>
                
                {item.description && (
                  <p className="text-gray-600 text-sm leading-relaxed">
                    {item.description}
                  </p>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MenuSection;