/**
 * Navigation Routes
 * Centralized route constants for TAUROS app
 */

export const ROUTES = {
  CHAT: 'Chat',
  STATUS: 'Status',
  SETTINGS: 'Settings',
} as const;

export type Route = typeof ROUTES[keyof typeof ROUTES];

// Screen Configuration
export const SCREEN_OPTIONS = {
  headerShown: false,
  gestureEnabled: true,
  animationTypeForReplace: 'push',
} as const;
