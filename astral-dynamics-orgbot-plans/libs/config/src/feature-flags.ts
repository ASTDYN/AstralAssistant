export const featureFlags = {
  sentryLookup: process.env.ENABLE_SENTRY_LOOKUP === 'true',
  rsiPublicLookup: process.env.ENABLE_RSI_PUBLIC_LOOKUP === 'true',
  starCitizenWikiLookup: process.env.ENABLE_STAR_CITIZEN_WIKI_LOOKUP !== 'false',
  vehicleRegistry: false,
  fleetPlanning: false,
  treasury: false,
  training: false,
  diplomacy: false,
  orgHealthAnalytics: false,
};

export type FeatureFlags = typeof featureFlags;
