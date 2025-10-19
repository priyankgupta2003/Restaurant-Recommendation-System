# Restaurant Finder - Frontend

Modern Next.js frontend for the Restaurant Recommendation System.

## Features

- 🎨 Beautiful, responsive UI with Tailwind CSS
- 💬 Real-time chat interface
- 🍽️ Restaurant cards with images, ratings, and reviews
- 📍 Location detection and management
- 🔄 React Query for data fetching
- 📱 Mobile-responsive design

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Icons**: Lucide React
- **HTTP Client**: Axios

## Prerequisites

- Node.js 18+ 
- npm or yarn

## Installation

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Set up environment variables**
```bash
# Create .env.local file
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

3. **Run development server**
```bash
npm run dev
```

4. **Open in browser**
```
http://localhost:3000
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app router pages
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Home page
│   │   ├── providers.tsx # React Query provider
│   │   └── globals.css   # Global styles
│   ├── components/       # React components
│   │   ├── Chat/         # Chat interface components
│   │   └── Restaurant/   # Restaurant components
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API services
│   └── types/            # TypeScript types
├── public/               # Static assets
└── package.json
```

## Components

### ChatInterface
Main chat interface with message history and restaurant results

### MessageList
Displays conversation messages

### InputBox
Text input with send button

### RestaurantCard
Restaurant card with image, rating, reviews, and details

### RestaurantList
Grid of restaurant cards

## Hooks

### useChat
Manages chat state and message sending

### useLocation
Handles user location detection and management

## API Service

The `apiService` handles all backend communication:

```typescript
- sendMessage(request: ChatRequest)
- searchRestaurants(params: RestaurantSearchParams)
- getRestaurantDetails(restaurantId: string)
- getNearbyRestaurants(lat, lng)
```

## Customization

### Styling

Edit `tailwind.config.js` to customize colors and theme:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your brand colors
      },
    },
  },
}
```

### API URL

Change backend URL in `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## Building for Production

```bash
npm run build
npm start
```

## Docker

Build Docker image:

```bash
docker build -t restaurant-frontend .
docker run -p 3000:3000 restaurant-frontend
```

## Troubleshooting

### API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running
- Check CORS settings on backend

### Location Not Working
- Ensure HTTPS (or localhost for development)
- Check browser permissions
- Verify Google Maps API key

## Contributing

1. Create a feature branch
2. Make changes
3. Run linting and type checking
4. Submit pull request

## License

MIT License

