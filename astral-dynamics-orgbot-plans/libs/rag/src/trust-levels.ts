export type TrustLevel =
  | 'official_org_policy'
  | 'org_lore'
  | 'external_game_info'
  | 'community_tip'
  | 'admin_private';

export type Audience = 'public' | 'member' | 'admin';

export const KB_FOLDER_TO_DEFAULT_TRUST: Record<string, TrustLevel> = {
  org: 'official_org_policy',
  'star-citizen': 'external_game_info',
  'admin-private': 'admin_private',
};

export const TRUST_LEVEL_TO_AUDIENCE: Record<TrustLevel, Audience> = {
  official_org_policy: 'public',
  org_lore: 'public',
  external_game_info: 'public',
  community_tip: 'public',
  admin_private: 'admin',
};
