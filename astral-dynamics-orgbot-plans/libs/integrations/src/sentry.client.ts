import { Inject, Injectable, Logger } from '@nestjs/common';

import { FEATURE_FLAGS, type FeatureFlags } from '@astral/config';

/**
 * SENTRY here refers to the Star Citizen community lookup service for public
 * RSI handle / org enrichment. It is NOT Sentry.io error tracking.
 *
 * Off by default. Must never be used as proof of identity.
 */
@Injectable()
export class SentryClient {
  private readonly logger = new Logger(SentryClient.name);

  constructor(@Inject(FEATURE_FLAGS) private readonly flags: FeatureFlags) {}

  isEnabled(): boolean {
    return this.flags.sentryLookup === true;
  }

  async lookupHandle(_handle: string): Promise<{ source: 'sentry'; result: null }> {
    if (!this.isEnabled()) {
      this.logger.debug('SENTRY lookup is disabled by feature flag.');
      return { source: 'sentry', result: null };
    }
    return { source: 'sentry', result: null };
  }
}
