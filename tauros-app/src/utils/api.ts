/**
 * API Utilities
 * Centralized API communication for TAUROS app
 * Integrates with FastAPI backend, Redis, and Ollama
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

// Storage keys
const STORAGE_KEYS = {
  BACKEND_URL: 'tauros_backend_url',
  AI_MODEL: 'tauros_ai_model',
  CHAT_HISTORY: 'tauros_chat_history',
  NOTIFICATIONS: 'tauros_notifications',
} as const;

// Default configuration
const DEFAULT_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  TIMEOUT: 30000,
  AI_MODEL: 'llama3',
} as const;

// Available AI models
export const AI_MODELS = [
  { id: 'llama3', name: 'Llama 3', description: 'Modello principale' },
  { id: 'mistral', name: 'Mistral', description: 'Veloce e preciso' },
  { id: 'codellama', name: 'CodeLlama', description: 'Ottimizzato per codice' },
  { id: 'phi3', name: 'Phi-3', description: 'Compatto ed efficiente' },
  { id: 'gemma', name: 'Gemma', description: 'Google AI' },
] as const;

export type AIModelId = typeof AI_MODELS[number]['id'];

// Helper to validate AI model ID
const isValidAIModel = (model: string): model is AIModelId => {
  return AI_MODELS.some(m => m.id === model);
};

// Helper to validate and normalize backend URLs
const validateBackendUrl = (url: string): string => {
  const trimmedUrl = url.trim();

  try {
    const parsed = new URL(trimmedUrl);

    // Only allow HTTP(S) backends
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
      throw new Error('Invalid protocol for backend URL');
    }

    // Return a normalized URL string (remove trailing slash)
    return parsed.origin + parsed.pathname.replace(/\/$/, '');
  } catch {
    throw new Error('Invalid backend URL');
  }
};

// Request/Response types
export interface ChatRequest {
  message: string;
  model?: string;
}

export interface ChatResponse {
  response: string;
  model?: string;
  timestamp?: string;
}

export interface ServiceStatus {
  name: string;
  status: 'online' | 'offline' | 'unknown';
  message?: string;
  latency?: number;
}

export interface HealthCheckResponse {
  status: string;
  services: {
    telegram_bot?: boolean;
    fastapi?: boolean;
    redis?: boolean;
    ollama?: boolean;
  };
  timestamp?: string;
}

export interface ChatMessage {
  id: string;
  message: string;
  response: string;
  timestamp: Date;
  model?: string;
}

// Custom API Error class
export class APIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }

  get isTimeoutError(): boolean {
    return this.code === 'TIMEOUT';
  }

  get isNetworkError(): boolean {
    return this.statusCode === 0 || !this.statusCode;
  }

  get isServerError(): boolean {
    return this.statusCode >= 500;
  }

  get isClientError(): boolean {
    return this.statusCode >= 400 && this.statusCode < 500;
  }

  getUserMessage(): string {
    if (this.isTimeoutError) {
      return 'Timeout della richiesta. Riprova.';
    }
    if (this.isNetworkError) {
      return 'Impossibile connettersi al server.';
    }
    if (this.isServerError) {
      return 'Errore interno del server.';
    }
    if (this.isClientError) {
      return 'Richiesta non valida.';
    }
    return 'Errore nel contatto con TAUROS.';
  }
}

// Settings API
export const settingsAPI = {
  getBackendUrl: async (): Promise<string> => {
    try {
      const url = await AsyncStorage.getItem(STORAGE_KEYS.BACKEND_URL);
      if (!url) {
        return DEFAULT_CONFIG.BASE_URL;
      }

      try {
        return validateBackendUrl(url);
      } catch {
        // If the stored URL is invalid, fall back to default
        return DEFAULT_CONFIG.BASE_URL;
      }
    } catch {
      return DEFAULT_CONFIG.BASE_URL;
    }
  },

  setBackendUrl: async (url: string): Promise<void> => {
    const validatedUrl = validateBackendUrl(url);
    await AsyncStorage.setItem(STORAGE_KEYS.BACKEND_URL, validatedUrl);
  },

  getAIModel: async (): Promise<AIModelId> => {
    try {
      const model = await AsyncStorage.getItem(STORAGE_KEYS.AI_MODEL);
      if (model && isValidAIModel(model)) {
        return model;
      }
      return DEFAULT_CONFIG.AI_MODEL;
    } catch {
      return DEFAULT_CONFIG.AI_MODEL;
    }
  },

  setAIModel: async (model: AIModelId): Promise<void> => {
    await AsyncStorage.setItem(STORAGE_KEYS.AI_MODEL, model);
  },

  getNotifications: async (): Promise<boolean> => {
    try {
      const value = await AsyncStorage.getItem(STORAGE_KEYS.NOTIFICATIONS);
      return value !== 'false'; // Default to true
    } catch {
      return true;
    }
  },

  setNotifications: async (enabled: boolean): Promise<void> => {
    await AsyncStorage.setItem(STORAGE_KEYS.NOTIFICATIONS, String(enabled));
  },
};

// Fetch with timeout helper
const fetchWithTimeout = async (
  url: string,
  options: RequestInit,
  timeout: number = DEFAULT_CONFIG.TIMEOUT
): Promise<Response> => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new APIError('Request timeout', 0, 'TIMEOUT');
    }
    throw error;
  }
};

// Chat API
export const chatAPI = {
  sendMessage: async (message: string): Promise<ChatResponse> => {
    const baseUrl = await settingsAPI.getBackendUrl();
    const model = await settingsAPI.getAIModel();

    try {
      const response = await fetchWithTimeout(
        `${baseUrl}/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message, model }),
        }
      );

      if (!response.ok) {
        throw new APIError(
          `HTTP Error: ${response.status}`,
          response.status
        );
      }

      const data = await response.json();
      return {
        response: data.response || 'Risposta non disponibile',
        model: data.model || model,
        timestamp: data.timestamp || new Date().toISOString(),
      };
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(
        error instanceof Error ? error.message : 'Errore sconosciuto',
        0
      );
    }
  },

  getChatHistory: async (): Promise<ChatMessage[]> => {
    try {
      const history = await AsyncStorage.getItem(STORAGE_KEYS.CHAT_HISTORY);
      if (history) {
        const parsed = JSON.parse(history);
        return parsed.map((msg: ChatMessage) => ({
          ...msg,
          timestamp: new Date(msg.timestamp),
        }));
      }
      return [];
    } catch {
      return [];
    }
  },

  saveChatMessage: async (message: ChatMessage): Promise<void> => {
    try {
      const history = await chatAPI.getChatHistory();
      history.push(message);
      // Keep only last 100 messages
      const trimmedHistory = history.slice(-100);
      await AsyncStorage.setItem(
        STORAGE_KEYS.CHAT_HISTORY,
        JSON.stringify(trimmedHistory)
      );
    } catch (error) {
      if (typeof __DEV__ !== 'undefined' && __DEV__) {
        console.error('Error saving chat message:', error);
      }
    }
  },

  clearChatHistory: async (): Promise<void> => {
    await AsyncStorage.removeItem(STORAGE_KEYS.CHAT_HISTORY);
  },
};

// Status API for service monitoring
export const statusAPI = {
  checkHealth: async (): Promise<HealthCheckResponse> => {
    const baseUrl = await settingsAPI.getBackendUrl();

    try {
      const response = await fetchWithTimeout(
        `${baseUrl}/health`,
        { method: 'GET' },
        5000 // Shorter timeout for health check
      );

      if (!response.ok) {
        throw new APIError(`HTTP Error: ${response.status}`, response.status);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(
        error instanceof Error ? error.message : 'Errore sconosciuto',
        0
      );
    }
  },

  getServiceStatuses: async (): Promise<ServiceStatus[]> => {
    const baseUrl = await settingsAPI.getBackendUrl();
    const services: ServiceStatus[] = [];

    // Check FastAPI
    const fastapiStart = Date.now();
    try {
      const response = await fetchWithTimeout(
        `${baseUrl}/health`,
        { method: 'GET' },
        5000
      );
      services.push({
        name: 'FastAPI',
        status: response.ok ? 'online' : 'offline',
        latency: Date.now() - fastapiStart,
      });
    } catch {
      services.push({
        name: 'FastAPI',
        status: 'offline',
        message: 'Impossibile connettersi',
      });
    }

    // Check Redis (via backend endpoint)
    try {
      const response = await fetchWithTimeout(
        `${baseUrl}/health/redis`,
        { method: 'GET' },
        5000
      );
      const data = await response.json();
      services.push({
        name: 'Redis',
        status: data.status === 'ok' ? 'online' : 'offline',
        message: data.message,
      });
    } catch {
      services.push({
        name: 'Redis',
        status: 'unknown',
        message: 'Stato sconosciuto',
      });
    }

    // Check Ollama (via backend endpoint)
    try {
      const response = await fetchWithTimeout(
        `${baseUrl}/health/ollama`,
        { method: 'GET' },
        5000
      );
      const data = await response.json();
      services.push({
        name: 'Ollama',
        status: data.status === 'ok' ? 'online' : 'offline',
        message: data.message,
      });
    } catch {
      services.push({
        name: 'Ollama',
        status: 'unknown',
        message: 'Stato sconosciuto',
      });
    }

    // Check Telegram Bot (via backend endpoint)
    try {
      const response = await fetchWithTimeout(
        `${baseUrl}/health/telegram`,
        { method: 'GET' },
        5000
      );
      const data = await response.json();
      services.push({
        name: 'Telegram Bot',
        status: data.status === 'ok' ? 'online' : 'offline',
        message: data.message,
      });
    } catch {
      services.push({
        name: 'Telegram Bot',
        status: 'unknown',
        message: 'Stato sconosciuto',
      });
    }

    return services;
  },

  testConnection: async (): Promise<{ success: boolean; message: string; latency?: number }> => {
    const baseUrl = await settingsAPI.getBackendUrl();
    const startTime = Date.now();

    try {
      const response = await fetchWithTimeout(
        `${baseUrl}/health`,
        { method: 'GET' },
        5000
      );

      const latency = Date.now() - startTime;

      if (response.ok) {
        return {
          success: true,
          message: `Connesso con successo (${latency}ms)`,
          latency,
        };
      } else {
        return {
          success: false,
          message: `Errore HTTP: ${response.status}`,
        };
      }
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Errore di connessione',
      };
    }
  },
};
