/**
 * App.tsx - Main Application Entry Point
 * TAUROS - Companion app for Tauros AI Bot
 * 
 * Features:
 * - Chat interface for AI communication via REST API
 * - Status dashboard for service monitoring
 * - Settings for backend configuration
 * - Type-safe navigation with TypeScript
 */

import React, { Suspense, lazy } from 'react';
import { StatusBar } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// Theme and Constants
import { theme } from './src/theme';
import { ROUTES, SCREEN_OPTIONS } from './src/constants/routes';

// Types
import type { RootStackParamList } from './src/types/navigation';

// Components
import { Loading } from './src/components/Loading';
import { ErrorBoundary } from './src/components/ErrorBoundary';

// Lazy-loaded screens for optimal performance
const ChatScreen = lazy(() => 
  import('./src/screens/ChatScreen')
    .then(module => ({ 
      default: module.ChatScreen 
    }))
    .catch(error => {
      if (__DEV__) {
        console.error('Failed to load ChatScreen module', error);
      }
      throw error;
    })
);

const StatusScreen = lazy(() => 
  import('./src/screens/StatusScreen')
    .then(module => ({ 
      default: module.StatusScreen 
    }))
    .catch(error => {
      if (__DEV__) {
        console.error('Failed to load StatusScreen module', error);
      }
      throw error;
    })
);

const SettingsScreen = lazy(() => 
  import('./src/screens/SettingsScreen')
    .then(module => ({ 
      default: module.SettingsScreen 
    }))
    .catch(error => {
      if (__DEV__) {
        console.error('Failed to load SettingsScreen module', error);
      }
      throw error;
    })
);

// Stack Navigator
const Stack = createNativeStackNavigator<RootStackParamList>();

// Custom loading fallback component
const LoadingFallback: React.FC = () => (
  <Loading message="Caricamento schermata..." size="large" />
);

// Navigation theme configuration
const navigationTheme = {
  dark: true,
  colors: {
    primary: theme.colors.primary.accent,
    background: theme.colors.primary.background,
    card: theme.colors.primary.surface,
    text: theme.colors.text.primary,
    border: theme.colors.primary.border,
    notification: theme.colors.status.info,
  },
};

/**
 * Main App Component
 * Implements professional architecture with error boundaries,
 * lazy loading, and consistent theming
 */
const App: React.FC = () => {
  return (
    <ErrorBoundary fallbackMessage="Errore nell'inizializzazione dell'app">
      {/* Status Bar Configuration */}
      <StatusBar 
        barStyle="light-content" 
        backgroundColor={theme.colors.primary.background}
        translucent={false}
      />
      
      {/* Navigation Container */}
      <NavigationContainer theme={navigationTheme}>
        <Stack.Navigator
          initialRouteName={ROUTES.CHAT}
          screenOptions={SCREEN_OPTIONS}
        >
          {/* Chat Screen - Main Entry Point */}
          <Stack.Screen 
            name={ROUTES.CHAT}
            options={{
              title: 'TAUROS Chat',
              headerShown: false,
            }}
          >
            {(props) => (
              <ErrorBoundary fallbackMessage="Errore nel caricamento della chat">
                <Suspense fallback={<LoadingFallback />}>
                  <ChatScreen {...props} />
                </Suspense>
              </ErrorBoundary>
            )}
          </Stack.Screen>

          {/* Status Screen - Service Monitoring */}
          <Stack.Screen 
            name={ROUTES.STATUS}
            options={{
              title: 'Status Servizi',
              headerShown: false,
            }}
          >
            {(props) => (
              <ErrorBoundary fallbackMessage="Errore nel caricamento dello status">
                <Suspense fallback={<LoadingFallback />}>
                  <StatusScreen {...props} />
                </Suspense>
              </ErrorBoundary>
            )}
          </Stack.Screen>

          {/* Settings Screen */}
          <Stack.Screen 
            name={ROUTES.SETTINGS}
            options={{
              title: 'Impostazioni',
              headerShown: false,
            }}
          >
            {(props) => (
              <ErrorBoundary fallbackMessage="Errore nel caricamento delle impostazioni">
                <Suspense fallback={<LoadingFallback />}>
                  <SettingsScreen {...props} />
                </Suspense>
              </ErrorBoundary>
            )}
          </Stack.Screen>
        </Stack.Navigator>
      </NavigationContainer>
    </ErrorBoundary>
  );
};

export default App;

/**
 * Export types for external usage
 */
export type { RootStackParamList } from './src/types/navigation';
