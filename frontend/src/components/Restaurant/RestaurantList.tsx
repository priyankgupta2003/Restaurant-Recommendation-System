/**
 * Restaurant list component
 */

'use client';

import React from 'react';
import { Restaurant } from '@/types/restaurant';
import RestaurantCard from './RestaurantCard';

interface RestaurantListProps {
  restaurants: Restaurant[];
}

export default function RestaurantList({ restaurants }: RestaurantListProps) {
  if (restaurants.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        <p>No restaurants found</p>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        Recommended Restaurants ({restaurants.length})
      </h2>
      {restaurants.map((restaurant) => (
        <RestaurantCard key={restaurant.id} restaurant={restaurant} />
      ))}
    </div>
  );
}

