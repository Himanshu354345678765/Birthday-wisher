# Birthday Reminder Frontend

React-based web interface for the Birthday Reminder application.

## Features

- Modern, responsive React interface
- Contact management with search and filtering
- Settings configuration for Twilio integration
- Dashboard with birthday overview and scheduler controls
- Real-time status updates and notifications

## Installation

1. **Install Dependencies**:
   \`\`\`bash
   npm install
   \`\`\`

2. **Start Development Server**:
   \`\`\`bash
   npm start
   \`\`\`

3. **Build for Production**:
   \`\`\`bash
   npm run build
   \`\`\`

## Dependencies

### Core
- `react` - UI framework
- `react-dom` - DOM rendering
- `react-router-dom` - Client-side routing

### Utilities
- `axios` - HTTP client
- `date-fns` - Date manipulation
- `lucide-react` - Icon library

## Project Structure

\`\`\`
src/
├── components/
│   └── Layout.js          # Main layout component
├── pages/
│   ├── Dashboard.js       # Dashboard page
│   ├── Contacts.js        # Contact management
│   └── Settings.js        # Settings configuration
├── App.js                 # Main application
├── App.css               # Application styles
└── index.js              # Entry point
\`\`\`

## Configuration

The frontend is configured to proxy API requests to `http://localhost:5000` during development.

For production, update the API base URL in the axios configuration.

## Styling

The application uses:
- CSS custom properties for theming
- Flexbox for layouts
- Responsive design principles
- Modern color palette with semantic tokens

## Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+
