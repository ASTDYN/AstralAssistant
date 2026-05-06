export const retentionConfig = {
  warningsDays: Number(process.env.RETENTION_WARNINGS_DAYS ?? 30),
  incidentsDays: Number(process.env.RETENTION_INCIDENTS_DAYS ?? 60),
  adminNotesDays: Number(process.env.RETENTION_ADMIN_NOTES_DAYS ?? 90),
  auditLogsDays: Number(process.env.RETENTION_AUDIT_LOGS_DAYS ?? 365),
  applicationPrivateNotesDays: Number(process.env.RETENTION_APPLICATION_PRIVATE_NOTES_DAYS ?? 90),
};

export type RetentionConfig = typeof retentionConfig;
