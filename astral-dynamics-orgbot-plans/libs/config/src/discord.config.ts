export type DiscordChannelConfig = {
  onboardingChannelId?: string;
  adminLogChannelId?: string;
  operationsChannelId?: string;
  botOutputChannelId?: string;
  rulesChannelId?: string;
  announcementsChannelId?: string;
};

export type DiscordRoleConfig = {
  adminRoleId?: string;
  memberRoleId?: string;
  recruitRoleId?: string;
  trialMemberRoleId?: string;
  botManagerRoleId?: string;
};

export const discordConfig = {
  botToken: process.env.DISCORD_BOT_TOKEN,
  clientId: process.env.DISCORD_CLIENT_ID,
  guildId: process.env.DISCORD_GUILD_ID,
  channels: {
    onboardingChannelId: process.env.DISCORD_ONBOARDING_CHANNEL_ID,
    adminLogChannelId: process.env.DISCORD_ADMIN_LOG_CHANNEL_ID,
    operationsChannelId: process.env.DISCORD_OPS_CHANNEL_ID,
    botOutputChannelId: process.env.DISCORD_BOT_OUTPUT_CHANNEL_ID,
    rulesChannelId: process.env.DISCORD_RULES_CHANNEL_ID,
    announcementsChannelId: process.env.DISCORD_ANNOUNCEMENTS_CHANNEL_ID,
  } satisfies DiscordChannelConfig,
  roles: {
    adminRoleId: process.env.DISCORD_ADMIN_ROLE_ID,
    memberRoleId: process.env.DISCORD_MEMBER_ROLE_ID,
    recruitRoleId: process.env.DISCORD_RECRUIT_ROLE_ID,
    trialMemberRoleId: process.env.DISCORD_TRIAL_MEMBER_ROLE_ID,
    botManagerRoleId: process.env.DISCORD_BOT_MANAGER_ROLE_ID,
  } satisfies DiscordRoleConfig,
};

export type DiscordConfig = typeof discordConfig;
