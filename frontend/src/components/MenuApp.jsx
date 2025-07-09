import React from 'react';
import MenuHeader from './MenuHeader';
import NavigationMenu from './NavigationMenu';
import MenuSection from './MenuSection';
import { menuData } from '../data/mockData';

const MenuApp = () => {
  return (
    <div className="min-h-screen bg-white">
      <MenuHeader />
      <NavigationMenu />
      
      <main>
        <MenuSection category="apericena" items={menuData.apericena} />
        <MenuSection category="bevande" items={menuData.bevande} />
        <MenuSection category="vini" items={menuData.vini} />
        <MenuSection category="mixology" items={menuData.mixology} />
        <MenuSection category="gin" items={menuData.gin} />
      </main>
      
      <footer className="bg-amber-900 text-amber-100 py-8 mt-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h3 className="text-2xl font-bold mb-2">Menù 9nove</h3>
          <p className="text-amber-300">
            Aperitivo • Cocktails • Vini
          </p>
          <div className="mt-4 flex items-center justify-center space-x-4 text-amber-400">
            <div className="w-12 h-px bg-amber-600"></div>
            <span className="text-xl">🍷</span>
            <div className="w-12 h-px bg-amber-600"></div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default MenuApp;