import { Module } from '@nestjs/common';

import { ConfigModule } from '@astral/config';
import { CoreModule } from '@astral/core';
import { DbModule } from '@astral/db';
import { IntegrationsModule } from '@astral/integrations';
import { RagModule } from '@astral/rag';

import { HealthController } from './health/health.controller';

@Module({
  imports: [ConfigModule, DbModule, CoreModule, IntegrationsModule, RagModule],
  controllers: [HealthController],
  providers: [],
})
export class ApiModule {}
