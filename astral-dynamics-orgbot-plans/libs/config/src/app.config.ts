export type AppRuntime = 'development' | 'test' | 'production';

export const appConfig = {
  nodeEnv: (process.env.NODE_ENV ?? 'development') as AppRuntime,
  appName: process.env.APP_NAME ?? 'AstralDynamics OrgBot',
  apiPort: Number(process.env.API_PORT ?? 3000),
  apiBaseUrl: process.env.API_BASE_URL ?? 'http://localhost:3000',
  databaseUrl: process.env.DATABASE_URL ?? '',
  kbRoot: process.env.KB_ROOT ?? './kb',
  ragEnabled: process.env.ENABLE_RAG !== 'false',
};

export type AppConfig = typeof appConfig;
