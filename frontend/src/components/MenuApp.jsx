import React from 'react';
import MenuHeader from './MenuHeader';
import NavigationMenu from './NavigationMenu';
import MenuSection from './MenuSection';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import { useMenu } from '../hooks/useMenu';

const MenuApp = () => {
  const { menuData, loading, error, refreshMenu } = useMenu();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={refreshMenu} />;
  }

  return (
    <div className="min-h-screen bg-white">
      <MenuHeader />
      <NavigationMenu categories={menuData} />
      
      <main>
        {menuData.map((category) => (
          <MenuSection 
            key={category.id}
            category={category.id}
            title={category.label}
            icon={category.icon}
            items={category.items}
          />
        ))}
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