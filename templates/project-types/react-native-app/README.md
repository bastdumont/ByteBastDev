# React Native Mobile App

Cross-platform mobile application for iOS and Android using React Native, TypeScript, and Firebase.

## Overview

A complete mobile app with:
- **React Native**: Cross-platform development
- **Expo**: Easy development and deployment
- **TypeScript**: Type safety
- **Firebase**: Real-time backend
- **Redux**: State management
- **React Navigation**: Routing

## Features

✅ **Cross-Platform**
- iOS and Android
- Single codebase
- Native performance

✅ **Authentication**
- Firebase Auth
- Social login ready
- Secure token storage

✅ **Real-time Data**
- Firebase Realtime DB
- Live updates
- Offline support

✅ **UI**
- Native components
- Responsive design
- Dark mode

✅ **Navigation**
- Stack navigation
- Tab navigation
- Deep linking

## Quick Start

### Prerequisites
```bash
Node.js >= 18.0.0
npm >= 9.0.0
Expo CLI: npm install -g expo-cli
```

### Installation

```bash
npm install
cp .env.example .env
expo start
```

### Run on Devices

```bash
expo start --ios     # iOS Simulator
expo start --android # Android Emulator
```

## Project Structure

```
react-native-app/
├── src/
│   ├── navigation/   # Navigation setup
│   ├── screens/      # Screen components
│   ├── components/   # Reusable components
│   ├── store/        # Redux store
│   ├── services/     # API/Firebase
│   └── styles/       # Styling
├── app.json          # Expo config
├── package.json
└── README.md
```

## Development

```bash
expo start           # Start dev server
expo publish         # Publish to Expo
npm run test         # Run tests
```

## Deployment

### iOS

```bash
eas build --platform ios
eas submit --platform ios
```

### Android

```bash
eas build --platform android
eas submit --platform android
```

---

**Build amazing mobile apps!** 📱
