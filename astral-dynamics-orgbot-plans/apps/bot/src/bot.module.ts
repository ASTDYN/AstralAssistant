import { Module } from '@nestjs/common';

import { ConfigModule } from '@astral/config';
import { CoreModule } from '@astral/core';
import { DbModule } from '@astral/db';
import { IntegrationsModule } from '@astral/integrations';
import { RagModule } from '@astral/rag';

@Module({
  imports: [ConfigModule, DbModule, CoreModule, IntegrationsModule, RagModule],
  providers: [],
})
export class BotModule {}
