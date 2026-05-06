import { Injectable, Logger } from '@nestjs/common';

import type { Audience } from './trust-levels';

/**
 * Phase 1 placeholder. Real KB ingest + retrieval lands in the dedicated RAG phase.
 *
 * Contract for that phase:
 * - load markdown from KB_ROOT
 * - tag each document with a TrustLevel based on folder
 * - filter results by caller audience (public / member / admin)
 * - never return admin_private documents to non-admin audiences
 */
@Injectable()
export class RagService {
  private readonly logger = new Logger(RagService.name);

  async ask(_question: string, _audience: Audience): Promise<{ answer: string; sources: never[] }> {
    this.logger.debug('RagService.ask called before RAG phase implementation.');
    return {
      answer: 'KB retrieval is not implemented yet.',
      sources: [],
    };
  }
}
