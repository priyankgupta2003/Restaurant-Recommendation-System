/**
 * Restaurant-related type definitions
 */

export interface Restaurant {
  id: string;
  name: string;
  rating?: number;
  review_count?: number;
  price?: string;
  categories?: Category[];
  location?: RestaurantLocation;
  phone?: string;
  image_url?: string;
  url?: string;
  is_closed?: boolean;
  distance?: number;
  reviews?: Review[];
}

export interface Category {
  alias: string;
  title: string;
}

export interface RestaurantLocation {
  address1?: string;
  address2?: string;
  address3?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  display_address?: string[];
}

export interface Review {
  id: string;
  rating: number;
  text: string;
  time_created: string;
  user?: {
    name?: string;
    image_url?: string;
  };
}

export interface RestaurantSearchParams {
  query?: string;
  location?: string;
  latitude?: number;
  longitude?: number;
  categories?: string;
  price?: string;
  radius?: number;
  limit?: number;
  sort_by?: string;
}

