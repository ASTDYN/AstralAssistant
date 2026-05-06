import { appConfig, featureFlags, orgConfig, retentionConfig, validateEnv } from '@astral/config';

describe('config boundaries', () => {
  it('exposes appConfig with sane defaults', () => {
    expect(appConfig.appName).toBe('AstralDynamics OrgBot');
    expect(typeof appConfig.apiPort).toBe('number');
  });

  it('matches the locked rank labels #1 through #5', () => {
    expect(orgConfig.rankLabels).toEqual(['#1', '#2', '#3', '#4', '#5']);
  });

  it('matches the V1 retention defaults', () => {
    expect(retentionConfig.warningsDays).toBe(30);
    expect(retentionConfig.incidentsDays).toBe(60);
    expect(retentionConfig.adminNotesDays).toBe(90);
  });

  it('keeps SENTRY and RSI public lookup off by default', () => {
    expect(featureFlags.sentryLookup).toBe(false);
    expect(featureFlags.rsiPublicLookup).toBe(false);
  });

  it('keeps deferred V1 modules disabled', () => {
    expect(featureFlags.vehicleRegistry).toBe(false);
    expect(featureFlags.fleetPlanning).toBe(false);
    expect(featureFlags.treasury).toBe(false);
    expect(featureFlags.training).toBe(false);
    expect(featureFlags.diplomacy).toBe(false);
    expect(featureFlags.orgHealthAnalytics).toBe(false);
  });
});

describe('env validation', () => {
  it('accepts an empty env and applies defaults', () => {
    const env = validateEnv({});
    expect(env.NODE_ENV).toBe('development');
    expect(env.API_PORT).toBe(3000);
    expect(env.RETENTION_WARNINGS_DAYS).toBe(30);
    expect(env.ENABLE_SENTRY_LOOKUP).toBe(false);
    expect(env.ENABLE_RSI_PUBLIC_LOOKUP).toBe(false);
    expect(env.ENABLE_STAR_CITIZEN_WIKI_LOOKUP).toBe(true);
  });

  it('coerces stringly-typed retention windows', () => {
    const env = validateEnv({
      RETENTION_WARNINGS_DAYS: '14',
      RETENTION_INCIDENTS_DAYS: '45',
    });
    expect(env.RETENTION_WARNINGS_DAYS).toBe(14);
    expect(env.RETENTION_INCIDENTS_DAYS).toBe(45);
  });

  it('rejects an invalid NODE_ENV', () => {
    expect(() => validateEnv({ NODE_ENV: 'staging' })).toThrow(/Invalid environment configuration/);
  });
});
