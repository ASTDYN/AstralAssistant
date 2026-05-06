export const orgConfig = {
  orgName: process.env.ORG_NAME ?? 'AstralDynamics',
  rankLabels: ['#1', '#2', '#3', '#4', '#5'],
  defaultRulesOfEngagement: [
    'No firing weapons at spaceports.',
    'No firing on friendlies.',
    'No firing on civilians.',
    'No firing on non-aggressive NPCs or players.',
    'Defensive engagement is authorized if fired upon.',
    'Operation-specific rules may override this if explicitly stated by an admin.',
  ],
  defaultPayoutModel: 'Equal split based on overall haul.',
};

export type OrgConfig = typeof orgConfig;
