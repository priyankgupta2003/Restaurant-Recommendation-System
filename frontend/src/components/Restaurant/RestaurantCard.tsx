/**
 * Restaurant card component
 */

'use client';

import React from 'react';
import { Restaurant } from '@/types/restaurant';
import { Star, MapPin, DollarSign, Phone, ExternalLink } from 'lucide-react';

interface RestaurantCardProps {
  restaurant: Restaurant;
}

export default function RestaurantCard({ restaurant }: RestaurantCardProps) {
  const {
    name,
    rating,
    review_count,
    price,
    categories,
    location,
    phone,
    image_url,
    url,
    distance,
    reviews,
  } = restaurant;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
      {/* Image */}
      {image_url && (
        <div className="relative h-48 w-full">
          <img
            src={image_url}
            alt={name}
            className="w-full h-full object-cover"
          />
          {price && (
            <div className="absolute top-3 right-3 bg-white px-3 py-1 rounded-full text-sm font-semibold text-gray-700">
              {price}
            </div>
          )}
        </div>
      )}

      {/* Content */}
      <div className="p-4">
        {/* Name and Rating */}
        <div className="flex items-start justify-between mb-2">
          <h3 className="text-lg font-bold text-gray-800 flex-1">{name}</h3>
          {rating && (
            <div className="flex items-center gap-1 bg-yellow-50 px-2 py-1 rounded">
              <Star size={16} className="text-yellow-500 fill-yellow-500" />
              <span className="text-sm font-semibold text-gray-800">{rating}</span>
            </div>
          )}
        </div>

        {/* Categories */}
        {categories && categories.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {categories.map((category) => (
              <span
                key={category.alias}
                className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded"
              >
                {category.title}
              </span>
            ))}
          </div>
        )}

        {/* Review Count */}
        {review_count !== undefined && (
          <p className="text-sm text-gray-500 mb-3">{review_count} reviews</p>
        )}

        {/* Location */}
        {location && (
          <div className="flex items-start gap-2 text-sm text-gray-600 mb-2">
            <MapPin size={16} className="flex-shrink-0 mt-0.5" />
            <span>
              {location.address1}
              {location.city && `, ${location.city}`}
              {distance && ` • ${(distance / 1000).toFixed(1)} km`}
            </span>
          </div>
        )}

        {/* Phone */}
        {phone && (
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-3">
            <Phone size={16} />
            <span>{phone}</span>
          </div>
        )}

        {/* Reviews */}
        {reviews && reviews.length > 0 && (
          <div className="mt-4 pt-4 border-t">
            <p className="text-sm font-semibold text-gray-700 mb-2">Recent Reviews:</p>
            <div className="space-y-2">
              {reviews.slice(0, 2).map((review) => (
                <div key={review.id} className="text-sm">
                  <div className="flex items-center gap-1 mb-1">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        size={12}
                        className={
                          i < review.rating
                            ? 'text-yellow-500 fill-yellow-500'
                            : 'text-gray-300'
                        }
                      />
                    ))}
                  </div>
                  <p className="text-gray-600 line-clamp-2">{review.text}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* View on Yelp */}
        {url && (
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 flex items-center justify-center gap-2 w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
          >
            <span>View on Yelp</span>
            <ExternalLink size={16} />
          </a>
        )}
      </div>
    </div>
  );
}

