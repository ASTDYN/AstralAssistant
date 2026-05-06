import 'reflect-metadata';

import { Logger } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';

import { appConfig } from '@astral/config';

import { ApiModule } from './api.module';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(ApiModule, { bufferLogs: false });
  app.enableShutdownHooks();

  const port = appConfig.apiPort;
  await app.listen(port);
  Logger.log(`API listening on port ${port}`, 'Bootstrap');
}

bootstrap().catch((error) => {
  Logger.error('API failed to start', error as Error, 'Bootstrap');
  process.exit(1);
});
