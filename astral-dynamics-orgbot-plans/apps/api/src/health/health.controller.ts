import { Controller, Get, Inject } from '@nestjs/common';

import { APP_CONFIG, type AppConfig } from '@astral/config';

@Controller('health')
export class HealthController {
  constructor(@Inject(APP_CONFIG) private readonly app: AppConfig) {}

  @Get()
  check(): { status: 'ok'; appName: string; nodeEnv: string; uptimeSeconds: number } {
    return {
      status: 'ok',
      appName: this.app.appName,
      nodeEnv: this.app.nodeEnv,
      uptimeSeconds: Math.floor(process.uptime()),
    };
  }
}
