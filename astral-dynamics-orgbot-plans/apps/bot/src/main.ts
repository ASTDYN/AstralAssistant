import 'reflect-metadata';

import { Logger } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';

import { BotModule } from './bot.module';

/**
 * Phase 1 boot only.
 *
 * The Discord client lifecycle is intentionally not wired up here yet.
 * It will be owned by a provider inside BotModule in the bot-shell phase
 * so that login/logout, intents, and slash command dispatch are all
 * managed inside the Nest dependency graph.
 */
async function bootstrap(): Promise<void> {
  const app = await NestFactory.createApplicationContext(BotModule, { bufferLogs: false });
  app.enableShutdownHooks();
  Logger.log('Bot application context started (Discord client not yet wired).', 'Bootstrap');
}

bootstrap().catch((error) => {
  Logger.error('Bot failed to start', error as Error, 'Bootstrap');
  process.exit(1);
});
