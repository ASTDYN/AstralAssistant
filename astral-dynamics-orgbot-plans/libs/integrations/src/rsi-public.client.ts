import { Inject, Injectable, Logger } from '@nestjs/common';

import { FEATURE_FLAGS, type FeatureFlags } from '@astral/config';

/**
 * Read-only public RSI page lookup. Disabled by default.
 *
 * Hard rules (see docs/architecture/external-data-policy.md):
 * - Never scrape login-protected pages.
 * - Never collect RSI credentials.
 * - Never impersonate a user session.
 * - Never use as proof of identity.
 */
@Injectable()
export class RsiPublicClient {
  private readonly logger = new Logger(RsiPublicClient.name);

  constructor(@Inject(FEATURE_FLAGS) private readonly flags: FeatureFlags) {}

  isEnabled(): boolean {
    return this.flags.rsiPublicLookup === true;
  }

  async lookupCitizen(_handle: string): Promise<{ source: 'rsi-public'; result: null }> {
    if (!this.isEnabled()) {
      this.logger.debug('RSI public lookup is disabled by feature flag.');
      return { source: 'rsi-public', result: null };
    }
    return { source: 'rsi-public', result: null };
  }
}
