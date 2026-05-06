import { Module } from '@nestjs/common';

import { RsiPublicClient } from './rsi-public.client';
import { SentryClient } from './sentry.client';
import { StarCitizenWikiClient } from './star-citizen-wiki.client';

@Module({
  providers: [StarCitizenWikiClient, SentryClient, RsiPublicClient],
  exports: [StarCitizenWikiClient, SentryClient, RsiPublicClient],
})
export class IntegrationsModule {}
