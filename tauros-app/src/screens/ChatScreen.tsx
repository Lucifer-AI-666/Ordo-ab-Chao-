/**
 * Chat Screen
 * Main chat interface with TAUROS AI bot
 * Features REST API communication via /chat endpoint with local persistence
 */

import React, { useState, useCallback, useEffect } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  ScrollView,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { theme } from '../theme';
import { ChatScreenProps } from '../types/navigation';
import { ROUTES } from '../constants/routes';
import { chatAPI, APIError, ChatMessage } from '../utils/api';

export const ChatScreen: React.FC<ChatScreenProps> = ({ navigation }) => {
  // State Management
  const [message, setMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

  // Load chat history on mount
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const history = await chatAPI.getChatHistory();
        setChatHistory(history);
      } catch (error) {
        if (typeof __DEV__ !== 'undefined' && __DEV__) {
          console.error('Error loading chat history:', error);
        }
      }
    };
    loadHistory();
  }, []);

  // Handle message sending with proper error handling
  const handleSend = useCallback(async () => {
    if (!message.trim()) {
      Alert.alert('Attenzione', 'Inserisci un messaggio prima di inviare.');
      return;
    }

    const messageToSend = message.trim();
    setMessage('');
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage(messageToSend);
      const responseText = response.response || 'Risposta non disponibile';

      // Create and save message
      const newMessage: ChatMessage = {
        id: Date.now().toString(),
        message: messageToSend,
        response: responseText,
        timestamp: new Date(),
        model: response.model,
      };
      
      setChatHistory(prev => [...prev, newMessage]);
      await chatAPI.saveChatMessage(newMessage);

    } catch (error) {
      if (typeof __DEV__ !== 'undefined' && __DEV__) {
        console.error('Chat error:', error);
      }
      
      let errorMessage = 'Errore nel contatto con TAUROS.';
      if (error instanceof APIError) {
        errorMessage = error.getUserMessage();
      }
      
      Alert.alert('Errore', errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [message]);

  // Navigate to settings
  const handleNavigateToSettings = useCallback(() => {
    navigation.navigate(ROUTES.SETTINGS);
  }, [navigation]);

  // Navigate to status
  const handleNavigateToStatus = useCallback(() => {
    navigation.navigate(ROUTES.STATUS);
  }, [navigation]);

  // Handle input change
  const handleMessageChange = useCallback((text: string) => {
    setMessage(text);
  }, []);

  // Clear chat history
  const handleClearHistory = useCallback(async () => {
    Alert.alert(
      'Conferma',
      'Vuoi cancellare tutta la cronologia chat?',
      [
        { text: 'Annulla', style: 'cancel' },
        { 
          text: 'Cancella', 
          style: 'destructive',
          onPress: async () => {
            await chatAPI.clearChatHistory();
            setChatHistory([]);
          }
        },
      ]
    );
  }, []);

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>TAUROS</Text>
        <Text style={styles.subtitle}>AI Assistant</Text>
        <View style={styles.headerActions}>
          <TouchableOpacity 
            style={styles.headerButton}
            onPress={handleNavigateToStatus}
          >
            <Text style={styles.headerButtonText}>Status</Text>
          </TouchableOpacity>
          {chatHistory.length > 0 && (
            <TouchableOpacity 
              style={styles.headerButton}
              onPress={handleClearHistory}
            >
              <Text style={styles.headerButtonText}>Pulisci</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* Response Display */}
      <ScrollView 
        style={styles.responseContainer}
        contentContainerStyle={styles.responseContent}
        showsVerticalScrollIndicator={false}
      >
        {chatHistory.length > 0 ? (
          chatHistory.map((chat, index) => (
            <View key={chat.id} style={styles.chatBubbleContainer}>
              <View style={styles.userBubble}>
                <Text style={styles.userText}>{chat.message}</Text>
              </View>
              <View style={styles.aiBubble}>
                <Text style={styles.aiText}>{chat.response}</Text>
                {chat.model && (
                  <Text style={styles.modelTag}>Modello: {chat.model}</Text>
                )}
              </View>
            </View>
          ))
        ) : (
          <Text style={styles.placeholderText}>
            Ciao! Sono TAUROS, il tuo assistente AI. Scrivi un messaggio per iniziare la conversazione.
          </Text>
        )}
      </ScrollView>

      {/* Input Section */}
      <View style={styles.inputSection}>
        <TextInput
          style={styles.textInput}
          placeholder="Scrivi qui il tuo messaggio..."
          placeholderTextColor={theme.colors.input.placeholder}
          value={message}
          onChangeText={handleMessageChange}
          multiline
          maxLength={1000}
          editable={!isLoading}
        />
        
        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, styles.primaryButton, isLoading && styles.disabledButton]}
            onPress={handleSend}
            disabled={isLoading}
          >
            <Text style={styles.primaryButtonText}>
              {isLoading ? 'Invio...' : 'Invia'}
            </Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.button, styles.secondaryButton]}
            onPress={handleNavigateToSettings}
          >
            <Text style={styles.secondaryButtonText}>Impostazioni</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.primary.background,
  },
  header: {
    paddingTop: theme.spacing.xl,
    paddingHorizontal: theme.spacing.lg,
    paddingBottom: theme.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.primary.border,
  },
  title: {
    ...theme.typography.h1,
    color: theme.colors.primary.accent,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  subtitle: {
    ...theme.typography.bodySmall,
    color: theme.colors.text.secondary,
    textAlign: 'center',
    marginTop: theme.spacing.xs,
  },
  headerActions: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: theme.spacing.md,
    marginTop: theme.spacing.sm,
  },
  headerButton: {
    paddingVertical: theme.spacing.xs,
    paddingHorizontal: theme.spacing.sm,
  },
  headerButtonText: {
    ...theme.typography.bodySmall,
    color: theme.colors.primary.accent,
  },
  responseContainer: {
    flex: 1,
    paddingHorizontal: theme.spacing.lg,
  },
  responseContent: {
    paddingVertical: theme.spacing.lg,
    minHeight: '100%',
  },
  chatBubbleContainer: {
    marginBottom: theme.spacing.md,
  },
  userBubble: {
    backgroundColor: theme.colors.primary.accent,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.lg,
    borderBottomRightRadius: theme.borderRadius.sm,
    alignSelf: 'flex-end',
    maxWidth: '85%',
    marginBottom: theme.spacing.sm,
  },
  userText: {
    ...theme.typography.body,
    color: theme.colors.text.inverse,
  },
  aiBubble: {
    backgroundColor: theme.colors.primary.surface,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.lg,
    borderBottomLeftRadius: theme.borderRadius.sm,
    alignSelf: 'flex-start',
    maxWidth: '85%',
  },
  aiText: {
    ...theme.typography.body,
    color: theme.colors.text.primary,
    lineHeight: 24,
  },
  modelTag: {
    ...theme.typography.caption,
    color: theme.colors.text.muted,
    marginTop: theme.spacing.xs,
  },
  placeholderText: {
    ...theme.typography.body,
    color: theme.colors.text.muted,
    fontStyle: 'italic',
    textAlign: 'center',
    marginTop: theme.spacing.xxl,
  },
  inputSection: {
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.md,
    borderTopWidth: 1,
    borderTopColor: theme.colors.primary.border,
    backgroundColor: theme.colors.primary.surface,
  },
  textInput: {
    ...theme.typography.input,
    backgroundColor: theme.colors.input.background,
    color: theme.colors.text.primary,
    borderWidth: 1,
    borderColor: theme.colors.input.border,
    borderRadius: theme.borderRadius.md,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    minHeight: theme.layout.inputHeight,
    maxHeight: 120,
    textAlignVertical: 'top',
  },
  buttonContainer: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
    marginTop: theme.spacing.md,
  },
  button: {
    flex: 1,
    height: theme.layout.buttonHeight,
    borderRadius: theme.borderRadius.md,
    justifyContent: 'center',
    alignItems: 'center',
  },
  primaryButton: {
    backgroundColor: theme.colors.button.primary,
  },
  primaryButtonText: {
    ...theme.typography.button,
    color: theme.colors.text.inverse,
  },
  secondaryButton: {
    backgroundColor: theme.colors.button.secondary,
    borderWidth: 1,
    borderColor: theme.colors.primary.border,
  },
  secondaryButtonText: {
    ...theme.typography.button,
    color: theme.colors.text.primary,
  },
  disabledButton: {
    opacity: 0.6,
  },
});
