import { useState, useEffect } from 'react';
import { menuApi } from '../services/api';

export const useMenu = () => {
  const [menuData, setMenuData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMenuData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const categories = await menuApi.getMenuByCategories();
      setMenuData(categories);
    } catch (err) {
      setError(err.message || 'Failed to fetch menu data');
      console.error('Error fetching menu data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMenuData();
  }, []);

  const refreshMenu = () => {
    fetchMenuData();
  };

  return {
    menuData,
    loading,
    error,
    refreshMenu
  };
};

export const useMenuItems = (category = null) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchItems = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const menuItems = await menuApi.getMenuItems(category);
      setItems(menuItems);
    } catch (err) {
      setError(err.message || 'Failed to fetch menu items');
      console.error('Error fetching menu items:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, [category]);

  const refreshItems = () => {
    fetchItems();
  };

  return {
    items,
    loading,
    error,
    refreshItems
  };
};