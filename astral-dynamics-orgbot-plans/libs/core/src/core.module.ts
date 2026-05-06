import { Module } from '@nestjs/common';

import { AuditModule } from './audit/audit.module';
import { MembersModule } from './members/members.module';
import { ModerationModule } from './moderation/moderation.module';
import { OperationsModule } from './operations/operations.module';
import { PermissionsModule } from './permissions/permissions.module';
import { RanksModule } from './ranks/ranks.module';
import { RecruitmentModule } from './recruitment/recruitment.module';
import { RetentionModule } from './retention/retention.module';

@Module({
  imports: [
    MembersModule,
    RecruitmentModule,
    OperationsModule,
    RanksModule,
    PermissionsModule,
    ModerationModule,
    AuditModule,
    RetentionModule,
  ],
  exports: [
    MembersModule,
    RecruitmentModule,
    OperationsModule,
    RanksModule,
    PermissionsModule,
    ModerationModule,
    AuditModule,
    RetentionModule,
  ],
})
export class CoreModule {}
