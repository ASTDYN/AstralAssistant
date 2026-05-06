import { z } from 'zod';

const optionalString = z
  .string()
  .trim()
  .min(1)
  .optional()
  .or(z.literal('').transform(() => undefined));

const boolFromEnv = (defaultValue: boolean) =>
  z
    .union([z.boolean(), z.string()])
    .default(defaultValue)
    .transform((value) => {
      if (typeof value === 'boolean') return value;
      return value.toLowerCase() === 'true';
    });

export const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  APP_NAME: z.string().default('AstralDynamics OrgBot'),
  ORG_NAME: z.string().default('AstralDynamics'),

  DISCORD_BOT_TOKEN: optionalString,
  DISCORD_CLIENT_ID: optionalString,
  DISCORD_GUILD_ID: optionalString,

  DISCORD_ONBOARDING_CHANNEL_ID: optionalString,
  DISCORD_ADMIN_LOG_CHANNEL_ID: optionalString,
  DISCORD_OPS_CHANNEL_ID: optionalString,
  DISCORD_BOT_OUTPUT_CHANNEL_ID: optionalString,
  DISCORD_RULES_CHANNEL_ID: optionalString,
  DISCORD_ANNOUNCEMENTS_CHANNEL_ID: optionalString,

  DISCORD_ADMIN_ROLE_ID: optionalString,
  DISCORD_MEMBER_ROLE_ID: optionalString,
  DISCORD_RECRUIT_ROLE_ID: optionalString,
  DISCORD_TRIAL_MEMBER_ROLE_ID: optionalString,
  DISCORD_BOT_MANAGER_ROLE_ID: optionalString,

  DATABASE_URL: z
    .string()
    .min(1, 'DATABASE_URL is required')
    .default(
      'postgresql://astral:astral@127.0.0.1:5432/astral_dynamics?schema=public',
    ),

  API_PORT: z.coerce.number().int().positive().default(3000),
  API_BASE_URL: z.string().default('http://localhost:3000'),

  RETENTION_WARNINGS_DAYS: z.coerce.number().int().nonnegative().default(30),
  RETENTION_INCIDENTS_DAYS: z.coerce.number().int().nonnegative().default(60),
  RETENTION_ADMIN_NOTES_DAYS: z.coerce.number().int().nonnegative().default(90),
  RETENTION_AUDIT_LOGS_DAYS: z.coerce.number().int().nonnegative().default(365),
  RETENTION_APPLICATION_PRIVATE_NOTES_DAYS: z.coerce.number().int().nonnegative().default(90),

  ENABLE_SENTRY_LOOKUP: boolFromEnv(false),
  ENABLE_RSI_PUBLIC_LOOKUP: boolFromEnv(false),
  ENABLE_STAR_CITIZEN_WIKI_LOOKUP: boolFromEnv(true),

  ENABLE_RAG: boolFromEnv(true),
  KB_ROOT: z.string().default('./kb'),
});

export type Env = z.infer<typeof envSchema>;

export function validateEnv(input: Record<string, unknown>): Env {
  const result = envSchema.safeParse(input);
  if (!result.success) {
    const issues = result.error.issues.map((i) => `  - ${i.path.join('.')}: ${i.message}`).join('\n');
    throw new Error(`Invalid environment configuration:\n${issues}`);
  }
  return result.data;
}
