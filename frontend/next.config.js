/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['s3-media1.fl.yelpcdn.com', 's3-media2.fl.yelpcdn.com', 's3-media3.fl.yelpcdn.com', 's3-media4.fl.yelpcdn.com'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_GOOGLE_MAPS_API_KEY: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
  },
}

module.exports = nextConfig

