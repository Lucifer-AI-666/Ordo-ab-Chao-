/**
 * Status Screen
 * Dashboard for monitoring backend services
 * Features: Telegram Bot, FastAPI, Redis, Ollama status with pull-to-refresh
 */

import React, { useState, useCallback, useEffect } from 'react';
import { 
  View, 
  Text, 
  TouchableOpacity, 
  StyleSheet, 
  ScrollView,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { theme } from '../theme';
import { StatusScreenProps } from '../types/navigation';
import { statusAPI, ServiceStatus, settingsAPI } from '../utils/api';

export const StatusScreen: React.FC<StatusScreenProps> = ({ navigation }) => {
  // State Management
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [backendUrl, setBackendUrl] = useState<string>('');
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  // Load backend URL
  useEffect(() => {
    const loadBackendUrl = async () => {
      const url = await settingsAPI.getBackendUrl();
      setBackendUrl(url);
    };
    loadBackendUrl();
  }, []);

  // Fetch service statuses
  const fetchStatuses = useCallback(async () => {
    try {
      const statuses = await statusAPI.getServiceStatuses();
      setServices(statuses);
      setLastUpdated(new Date());
    } catch (error) {
      if (typeof __DEV__ !== 'undefined' && __DEV__) {
        console.error('Error fetching statuses:', error);
      }
      // Set all services as unknown on error
      setServices([
        { name: 'FastAPI', status: 'offline', message: 'Errore di connessione' },
        { name: 'Redis', status: 'unknown', message: 'Stato sconosciuto' },
        { name: 'Ollama', status: 'unknown', message: 'Stato sconosciuto' },
        { name: 'Telegram Bot', status: 'unknown', message: 'Stato sconosciuto' },
      ]);
    }
  }, []);

  // Initial load
  useEffect(() => {
    const loadStatuses = async () => {
      setIsLoading(true);
      await fetchStatuses();
      setIsLoading(false);
    };
    loadStatuses();
  }, [fetchStatuses]);

  // Handle pull-to-refresh
  const handleRefresh = useCallback(async () => {
    setIsRefreshing(true);
    await fetchStatuses();
    setIsRefreshing(false);
  }, [fetchStatuses]);

  // Navigate back
  const handleBackPress = useCallback(() => {
    navigation.goBack();
  }, [navigation]);

  // Get status color
  const getStatusColor = (status: ServiceStatus['status']): string => {
    switch (status) {
      case 'online':
        return theme.colors.status.online;
      case 'offline':
        return theme.colors.status.offline;
      default:
        return theme.colors.status.warning;
    }
  };

  // Get status icon
  const getStatusIcon = (status: ServiceStatus['status']): string => {
    switch (status) {
      case 'online':
        return '●';
      case 'offline':
        return '○';
      default:
        return '◐';
    }
  };

  // Get status text
  const getStatusText = (status: ServiceStatus['status']): string => {
    switch (status) {
      case 'online':
        return 'Online';
      case 'offline':
        return 'Offline';
      default:
        return 'Sconosciuto';
    }
  };

  // Render service card
  const renderServiceCard = (service: ServiceStatus) => (
    <View key={service.name} style={styles.serviceCard}>
      <View style={styles.serviceHeader}>
        <Text style={styles.serviceName}>{service.name}</Text>
        <View style={styles.statusBadge}>
          <Text style={[styles.statusIcon, { color: getStatusColor(service.status) }]}>
            {getStatusIcon(service.status)}
          </Text>
          <Text style={[styles.statusText, { color: getStatusColor(service.status) }]}>
            {getStatusText(service.status)}
          </Text>
        </View>
      </View>
      {service.message && (
        <Text style={styles.serviceMessage}>{service.message}</Text>
      )}
      {service.latency !== undefined && (
        <Text style={styles.serviceLatency}>Latenza: {service.latency}ms</Text>
      )}
    </View>
  );

  // Calculate overall status
  const getOverallStatus = (): { status: 'healthy' | 'degraded' | 'down'; text: string } => {
    const onlineCount = services.filter(s => s.status === 'online').length;
    const totalCount = services.length;

    if (onlineCount === totalCount && totalCount > 0) {
      return { status: 'healthy', text: 'Tutti i servizi sono operativi' };
    } else if (onlineCount > 0) {
      return { status: 'degraded', text: `${onlineCount}/${totalCount} servizi operativi` };
    } else {
      return { status: 'down', text: 'Servizi non disponibili' };
    }
  };

  const overallStatus = getOverallStatus();

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={handleBackPress}>
          <Text style={styles.backButtonText}>‹ Indietro</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Status Servizi</Text>
        <View style={styles.headerSpacer} />
      </View>

      {/* Content */}
      {isLoading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={theme.colors.primary.accent} />
          <Text style={styles.loadingText}>Controllo servizi...</Text>
        </View>
      ) : (
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl
              refreshing={isRefreshing}
              onRefresh={handleRefresh}
              tintColor={theme.colors.primary.accent}
              colors={[theme.colors.primary.accent]}
            />
          }
        >
          {/* Overall Status */}
          <View style={[
            styles.overallCard,
            overallStatus.status === 'healthy' && styles.overallHealthy,
            overallStatus.status === 'degraded' && styles.overallDegraded,
            overallStatus.status === 'down' && styles.overallDown,
          ]}>
            <Text style={styles.overallTitle}>Stato Sistema</Text>
            <Text style={styles.overallText}>{overallStatus.text}</Text>
          </View>

          {/* Backend URL */}
          <View style={styles.backendCard}>
            <Text style={styles.backendLabel}>Backend URL:</Text>
            <Text style={styles.backendUrl}>{backendUrl}</Text>
          </View>

          {/* Service List */}
          <View style={styles.servicesSection}>
            <Text style={styles.sectionTitle}>Servizi</Text>
            {services.map(renderServiceCard)}
          </View>

          {/* Last Updated */}
          {lastUpdated && (
            <Text style={styles.lastUpdated}>
              Ultimo aggiornamento: {lastUpdated.toLocaleTimeString('it-IT')}
            </Text>
          )}

          {/* Refresh Hint */}
          <Text style={styles.refreshHint}>
            Trascina verso il basso per aggiornare
          </Text>
        </ScrollView>
      )}
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    ...theme.typography.body,
    color: theme.colors.text.secondary,
    marginTop: theme.spacing.md,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.lg,
    paddingBottom: theme.spacing.xxl,
  },
  overallCard: {
    padding: theme.spacing.lg,
    borderRadius: theme.borderRadius.lg,
    marginBottom: theme.spacing.lg,
    alignItems: 'center',
  },
  overallHealthy: {
    backgroundColor: 'rgba(35, 134, 54, 0.2)',
    borderWidth: 1,
    borderColor: theme.colors.status.success,
  },
  overallDegraded: {
    backgroundColor: 'rgba(210, 153, 34, 0.2)',
    borderWidth: 1,
    borderColor: theme.colors.status.warning,
  },
  overallDown: {
    backgroundColor: 'rgba(218, 54, 51, 0.2)',
    borderWidth: 1,
    borderColor: theme.colors.status.error,
  },
  overallTitle: {
    ...theme.typography.h3,
    color: theme.colors.text.primary,
    marginBottom: theme.spacing.xs,
  },
  overallText: {
    ...theme.typography.body,
    color: theme.colors.text.secondary,
  },
  backendCard: {
    backgroundColor: theme.colors.primary.surface,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    marginBottom: theme.spacing.lg,
  },
  backendLabel: {
    ...theme.typography.bodySmall,
    color: theme.colors.text.secondary,
    marginBottom: theme.spacing.xs,
  },
  backendUrl: {
    ...theme.typography.body,
    color: theme.colors.primary.accent,
    fontFamily: theme.fonts.monospace,
  },
  servicesSection: {
    marginBottom: theme.spacing.lg,
  },
  sectionTitle: {
    ...theme.typography.h3,
    color: theme.colors.text.secondary,
    marginBottom: theme.spacing.md,
  },
  serviceCard: {
    backgroundColor: theme.colors.primary.surface,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    marginBottom: theme.spacing.sm,
    borderWidth: 1,
    borderColor: theme.colors.primary.border,
  },
  serviceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  serviceName: {
    ...theme.typography.body,
    color: theme.colors.text.primary,
    fontWeight: '600',
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: theme.spacing.xs,
  },
  statusIcon: {
    fontSize: 14,
  },
  statusText: {
    ...theme.typography.bodySmall,
    fontWeight: '500',
  },
  serviceMessage: {
    ...theme.typography.caption,
    color: theme.colors.text.muted,
    marginTop: theme.spacing.xs,
  },
  serviceLatency: {
    ...theme.typography.caption,
    color: theme.colors.text.secondary,
    marginTop: theme.spacing.xs,
  },
  lastUpdated: {
    ...theme.typography.caption,
    color: theme.colors.text.muted,
    textAlign: 'center',
    marginBottom: theme.spacing.sm,
  },
  refreshHint: {
    ...theme.typography.caption,
    color: theme.colors.text.muted,
    textAlign: 'center',
    fontStyle: 'italic',
  },
});
