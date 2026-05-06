import { Inject, Injectable, Logger } from '@nestjs/common';

import { FEATURE_FLAGS, type FeatureFlags } from '@astral/config';

@Injectable()
export class StarCitizenWikiClient {
  private readonly logger = new Logger(StarCitizenWikiClient.name);

  constructor(@Inject(FEATURE_FLAGS) private readonly flags: FeatureFlags) {}

  isEnabled(): boolean {
    return this.flags.starCitizenWikiLookup === true;
  }

  async lookup(_term: string): Promise<{ source: 'star-citizen-wiki'; result: null }> {
    if (!this.isEnabled()) {
      this.logger.debug('Star Citizen Wiki lookup is disabled by feature flag.');
      return { source: 'star-citizen-wiki', result: null };
    }
    return { source: 'star-citizen-wiki', result: null };
  }
}
