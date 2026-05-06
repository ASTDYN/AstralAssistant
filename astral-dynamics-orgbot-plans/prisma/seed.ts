import 'dotenv/config';

import { PrismaClient } from '@prisma/client';
import { demoMembers } from './seed-data/demo-members';
import { ranks } from './seed-data/ranks';
import { interestTags } from './seed-data/interest-tags';

const prisma = new PrismaClient();

async function main() {
  for (const rank of ranks) {
    await prisma.rank.upsert({
      where: { label: rank.label },
      update: rank,
      create: rank,
    });
  }

  for (const label of interestTags) {
    const slug = label.toLowerCase().replace(/\s+/g, '-');
    await prisma.interestTag.upsert({
      where: { slug },
      update: { label, enabled: true },
      create: { label, slug, sortOrder: interestTags.indexOf(label) + 1 },
    });
  }

  for (const member of demoMembers) {
    const user = await prisma.user.upsert({
      where: { discordUserId: member.discordUserId },
      update: {
        discordUsernameSnapshot: member.discordUsernameSnapshot,
        rsiHandle: member.rsiHandle,
        displayName: member.displayName,
      },
      create: {
        discordUserId: member.discordUserId,
        discordUsernameSnapshot: member.discordUsernameSnapshot,
        rsiHandle: member.rsiHandle,
        displayName: member.displayName,
      },
    });

    await prisma.memberProfile.upsert({
      where: { userId: user.id },
      update: {
        status: member.status as any,
        rankLabel: member.rankLabel,
        websiteRole: member.websiteRole as any,
      },
      create: {
        userId: user.id,
        status: member.status as any,
        rankLabel: member.rankLabel,
        websiteRole: member.websiteRole as any,
      },
    });
  }
}

main()
  .then(async () => prisma.$disconnect())
  .catch(async (error) => {
    console.error(error);
    await prisma.$disconnect();
    process.exit(1);
  });
