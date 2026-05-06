import { Global, Module } from '@nestjs/common';
import { ConfigModule as NestConfigModule } from '@nestjs/config';

import { appConfig } from './app.config';
import {
  APP_CONFIG,
  DISCORD_CONFIG,
  FEATURE_FLAGS,
  ORG_CONFIG,
  RETENTION_CONFIG,
} from './config.tokens';
import { discordConfig } from './discord.config';
import { validateEnv } from './env.schema';
import { featureFlags } from './feature-flags';
import { orgConfig } from './org.config';
import { retentionConfig } from './retention.config';

@Global()
@Module({
  imports: [
    NestConfigModule.forRoot({
      isGlobal: true,
      cache: true,
      validate: (raw) => validateEnv(raw),
    }),
  ],
  providers: [
    { provide: APP_CONFIG, useValue: appConfig },
    { provide: DISCORD_CONFIG, useValue: discordConfig },
    { provide: ORG_CONFIG, useValue: orgConfig },
    { provide: RETENTION_CONFIG, useValue: retentionConfig },
    { provide: FEATURE_FLAGS, useValue: featureFlags },
  ],
  exports: [APP_CONFIG, DISCORD_CONFIG, ORG_CONFIG, RETENTION_CONFIG, FEATURE_FLAGS],
})
export class ConfigModule {}
