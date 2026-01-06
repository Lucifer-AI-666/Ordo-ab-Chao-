/**
 * Settings Screen
 * Application settings and configuration for TAUROS app
 * Features: Backend URL config, AI model selection, connection test
 */

import React, { useState, useCallback, useEffect } from 'react';
import { 
  View, 
  Text, 
  TextInput,
  Switch, 
  TouchableOpacity, 
  StyleSheet, 
  ScrollView,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { theme } from '../theme';
import { SettingsScreenProps } from '../types/navigation';
import { settingsAPI, statusAPI, AI_MODELS, AIModelId } from '../utils/api';

export const SettingsScreen: React.FC<SettingsScreenProps> = ({ navigation }) => {
  // State Management
  const [backendUrl, setBackendUrl] = useState<string>('');
  const [selectedModel, setSelectedModel] = useState<AIModelId>('llama3');
  const [notifications, setNotifications] = useState<boolean>(true);
  const [isTesting, setIsTesting] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null);

  // Load settings on mount
  useEffect(() => {
    const loadSettings = async () => {
      const url = await settingsAPI.getBackendUrl();
      const model = await settingsAPI.getAIModel();
      setBackendUrl(url);
      setSelectedModel(model);
    };
    loadSettings();
  }, []);

  // Handle backend URL change
  const handleUrlChange = useCallback((text: string) => {
    setBackendUrl(text);
    setTestResult(null); // Clear test result when URL changes
  }, []);

  // Save backend URL
  const handleSaveUrl = useCallback(async () => {
    if (!backendUrl.trim()) {
      Alert.alert('Errore', 'Inserisci un URL valido');
      return;
    }

    try {
      await settingsAPI.setBackendUrl(backendUrl.trim());
      Alert.alert('Salvato', 'URL backend salvato con successo');
    } catch (error) {
      Alert.alert('Errore', 'Impossibile salvare l\'URL');
    }
  }, [backendUrl]);

  // Test connection
  const handleTestConnection = useCallback(async () => {
    setIsTesting(true);
    setTestResult(null);

    try {
      // Temporarily save the URL for testing
      await settingsAPI.setBackendUrl(backendUrl.trim());
      const result = await statusAPI.testConnection();
      setTestResult(result);
    } catch (error) {
      setTestResult({
        success: false,
        message: 'Errore durante il test di connessione',
      });
    } finally {
      setIsTesting(false);
    }
  }, [backendUrl]);

  // Handle model selection
  const handleModelSelect = useCallback(async (modelId: AIModelId) => {
    setSelectedModel(modelId);
    try {
      await settingsAPI.setAIModel(modelId);
    } catch (error) {
      Alert.alert('Errore', 'Impossibile salvare il modello');
    }
  }, []);

  // Handle notifications toggle
  const handleNotificationsToggle = useCallback((value: boolean) => {
    setNotifications(value);
  }, []);

  // Handle about press
  const handleAboutPress = useCallback(() => {
    Alert.alert(
      'TAUROS v1.0.0',
      'Companion app per Tauros AI Bot.\n\nIntegrazione con:\n• FastAPI Backend\n• Redis Caching\n• Ollama AI Models\n• Telegram Bot\n\nSviluppato con React Native & TypeScript.',
      [{ text: 'OK' }]
    );
  }, []);

  // Navigate back
  const handleBackPress = useCallback(() => {
    navigation.goBack();
  }, [navigation]);

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={handleBackPress}>
          <Text style={styles.backButtonText}>‹ Indietro</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Impostazioni</Text>
        <View style={styles.headerSpacer} />
      </View>

      {/* Settings List */}
      <ScrollView 
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Backend Configuration Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Configurazione Backend</Text>
          
          {/* Backend URL Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.inputLabel}>URL Backend Tauros AI</Text>
            <TextInput
              style={styles.textInput}
              value={backendUrl}
              onChangeText={handleUrlChange}
              placeholder="http://localhost:8000"
              placeholderTextColor={theme.colors.input.placeholder}
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="url"
            />
            <Text style={styles.inputHint}>
              Inserisci l'URL del tuo backend FastAPI
            </Text>
          </View>

          {/* Action Buttons */}
          <View style={styles.buttonRow}>
            <TouchableOpacity
              style={[styles.actionButton, styles.saveButton]}
              onPress={handleSaveUrl}
            >
              <Text style={styles.actionButtonText}>Salva</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.actionButton, styles.testButton, isTesting && styles.disabledButton]}
              onPress={handleTestConnection}
              disabled={isTesting}
            >
              {isTesting ? (
                <ActivityIndicator size="small" color={theme.colors.text.primary} />
              ) : (
                <Text style={styles.testButtonText}>Test Connessione</Text>
              )}
            </TouchableOpacity>
          </View>

          {/* Test Result */}
          {testResult && (
            <View style={[
              styles.testResult,
              testResult.success ? styles.testSuccess : styles.testError
            ]}>
              <Text style={styles.testResultText}>{testResult.message}</Text>
            </View>
          )}
        </View>

        {/* AI Model Selection Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Modello AI</Text>
          <Text style={styles.sectionDescription}>
            Seleziona il modello AI da utilizzare per le conversazioni
          </Text>
          
          {AI_MODELS.map((model) => (
            <TouchableOpacity
              key={model.id}
              style={[
                styles.modelOption,
                selectedModel === model.id && styles.modelOptionSelected
              ]}
              onPress={() => handleModelSelect(model.id)}
            >
              <View style={styles.modelInfo}>
                <Text style={[
                  styles.modelName,
                  selectedModel === model.id && styles.modelNameSelected
                ]}>
                  {model.name}
                </Text>
                <Text style={styles.modelDescription}>{model.description}</Text>
              </View>
              <View style={[
                styles.radioButton,
                selectedModel === model.id && styles.radioButtonSelected
              ]}>
                {selectedModel === model.id && (
                  <View style={styles.radioButtonInner} />
                )}
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {/* Preferences Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Preferenze</Text>
          
          <View style={styles.settingItem}>
            <View style={styles.settingTextContainer}>
              <Text style={styles.settingTitle}>Notifiche Push</Text>
              <Text style={styles.settingDescription}>
                Ricevi avvisi quando un servizio va offline
              </Text>
            </View>
            <Switch
              value={notifications}
              onValueChange={handleNotificationsToggle}
              trackColor={{
                false: theme.colors.input.border,
                true: theme.colors.primary.accent,
              }}
              thumbColor={
                notifications 
                  ? theme.colors.text.primary 
                  : theme.colors.text.secondary
              }
            />
          </View>

          <TouchableOpacity style={styles.settingItem} onPress={handleAboutPress}>
            <View style={styles.settingTextContainer}>
              <Text style={styles.settingTitle}>Informazioni</Text>
              <Text style={styles.settingDescription}>
                Versione app e dettagli sviluppatore
              </Text>
            </View>
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
        </View>

        {/* App Info */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            TAUROS AI Assistant
          </Text>
          <Text style={styles.footerSubtext}>
            Versione 1.0.0 • React Native + Expo
          </Text>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.primary.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: theme.spacing.xl,
    paddingHorizontal: theme.spacing.lg,
    paddingBottom: theme.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.primary.border,
  },
  backButton: {
    paddingVertical: theme.spacing.xs,
  },
  backButtonText: {
    ...theme.typography.body,
    color: theme.colors.primary.accent,
    fontSize: 18,
  },
  title: {
    ...theme.typography.h2,
    color: theme.colors.text.primary,
    flex: 1,
    textAlign: 'center',
  },
  headerSpacer: {
    width: 60,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: theme.spacing.xl,
  },
  section: {
    paddingHorizontal: theme.spacing.lg,
    paddingTop: theme.spacing.lg,
  },
  sectionTitle: {
    ...theme.typography.h3,
    color: theme.colors.text.secondary,
    marginBottom: theme.spacing.sm,
  },
  sectionDescription: {
    ...theme.typography.bodySmall,
    color: theme.colors.text.muted,
    marginBottom: theme.spacing.md,
  },
  inputContainer: {
    marginBottom: theme.spacing.md,
  },
  inputLabel: {
    ...theme.typography.bodySmall,
    color: theme.colors.text.secondary,
    marginBottom: theme.spacing.xs,
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
    height: theme.layout.inputHeight,
  },
  inputHint: {
    ...theme.typography.caption,
    color: theme.colors.text.muted,
    marginTop: theme.spacing.xs,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
    marginBottom: theme.spacing.md,
  },
  actionButton: {
    flex: 1,
    height: theme.layout.buttonHeight,
    borderRadius: theme.borderRadius.md,
    justifyContent: 'center',
    alignItems: 'center',
  },
  saveButton: {
    backgroundColor: theme.colors.button.primary,
  },
  actionButtonText: {
    ...theme.typography.button,
    color: theme.colors.text.inverse,
  },
  testButton: {
    backgroundColor: theme.colors.button.secondary,
    borderWidth: 1,
    borderColor: theme.colors.primary.border,
  },
  testButtonText: {
    ...theme.typography.button,
    color: theme.colors.text.primary,
  },
  disabledButton: {
    opacity: 0.6,
  },
  testResult: {
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    marginBottom: theme.spacing.md,
  },
  testSuccess: {
    backgroundColor: 'rgba(35, 134, 54, 0.2)',
    borderWidth: 1,
    borderColor: theme.colors.status.success,
  },
  testError: {
    backgroundColor: 'rgba(218, 54, 51, 0.2)',
    borderWidth: 1,
    borderColor: theme.colors.status.error,
  },
  testResultText: {
    ...theme.typography.bodySmall,
    color: theme.colors.text.primary,
    textAlign: 'center',
  },
  modelOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: theme.colors.primary.surface,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    marginBottom: theme.spacing.sm,
    borderWidth: 1,
    borderColor: theme.colors.primary.border,
  },
  modelOptionSelected: {
    borderColor: theme.colors.primary.accent,
  },
  modelInfo: {
    flex: 1,
  },
  modelName: {
    ...theme.typography.body,
    color: theme.colors.text.primary,
    fontWeight: '500',
  },
  modelNameSelected: {
    color: theme.colors.primary.accent,
  },
  modelDescription: {
    ...theme.typography.caption,
    color: theme.colors.text.muted,
    marginTop: theme.spacing.xs,
  },
  radioButton: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: theme.colors.primary.border,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioButtonSelected: {
    borderColor: theme.colors.primary.accent,
  },
  radioButtonInner: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: theme.colors.primary.accent,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: theme.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.primary.border,
  },
  settingTextContainer: {
    flex: 1,
    marginRight: theme.spacing.md,
  },
  settingTitle: {
    ...theme.typography.body,
    color: theme.colors.text.primary,
    fontWeight: '500',
  },
  settingDescription: {
    ...theme.typography.bodySmall,
    color: theme.colors.text.secondary,
    marginTop: theme.spacing.xs,
  },
  chevron: {
    ...theme.typography.h2,
    color: theme.colors.text.muted,
    fontWeight: '300',
  },
  footer: {
    alignItems: 'center',
    paddingHorizontal: theme.spacing.lg,
    paddingTop: theme.spacing.xxl,
  },
  footerText: {
    ...theme.typography.body,
    color: theme.colors.text.secondary,
    fontWeight: '600',
  },
  footerSubtext: {
    ...theme.typography.caption,
    color: theme.colors.text.muted,
    marginTop: theme.spacing.xs,
  },
});
