import React, { useState, useEffect } from 'react';

const NavigationMenu = ({ categories = [] }) => {
  const [activeSection, setActiveSection] = useState(categories[0]?.id || '');

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      const offset = 80;
      const elementPosition = element.offsetTop - offset;
      window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
      });
    }
  };

  useEffect(() => {
    const handleScroll = () => {
      const sections = categories.map(cat => cat.id);
      const currentSection = sections.find(section => {
        const element = document.getElementById(section);
        if (element) {
          const rect = element.getBoundingClientRect();
          return rect.top <= 100 && rect.bottom >= 100;
        }
        return false;
      });
      
      if (currentSection) {
        setActiveSection(currentSection);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [categories]);

  // Update active section when categories change
  useEffect(() => {
    if (categories.length > 0 && !activeSection) {
      setActiveSection(categories[0].id);
    }
  }, [categories, activeSection]);

  return (
    <div className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-amber-200">
      <div className="max-w-4xl mx-auto">
        <div className="flex overflow-x-auto scrollbar-hide py-4 px-4">
          <div className="flex space-x-1 min-w-max">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => scrollToSection(category.id)}
                className={`
                  flex items-center space-x-2 px-4 py-2 rounded-full text-sm font-medium
                  transition-all duration-300 whitespace-nowrap
                  ${activeSection === category.id
                    ? 'bg-amber-500 text-white shadow-lg transform scale-105'
                    : 'text-amber-700 hover:bg-amber-100 hover:text-amber-800'
                  }
                `}
              >
                <span className="text-base">{category.icon}</span>
                <span>{category.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default NavigationMenu;