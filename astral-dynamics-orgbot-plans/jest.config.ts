import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  rootDir: '.',
  roots: ['<rootDir>/apps', '<rootDir>/libs', '<rootDir>/test'],
  testRegex: '.*\\.spec\\.ts$',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'json'],
  moduleNameMapper: {
    '^@astral/core$': '<rootDir>/libs/core/src',
    '^@astral/core/(.*)$': '<rootDir>/libs/core/src/$1',
    '^@astral/db$': '<rootDir>/libs/db/src',
    '^@astral/db/(.*)$': '<rootDir>/libs/db/src/$1',
    '^@astral/config$': '<rootDir>/libs/config/src',
    '^@astral/config/(.*)$': '<rootDir>/libs/config/src/$1',
    '^@astral/integrations$': '<rootDir>/libs/integrations/src',
    '^@astral/integrations/(.*)$': '<rootDir>/libs/integrations/src/$1',
    '^@astral/rag$': '<rootDir>/libs/rag/src',
    '^@astral/rag/(.*)$': '<rootDir>/libs/rag/src/$1',
  },
  collectCoverageFrom: ['apps/**/*.ts', 'libs/**/*.ts', '!**/*.spec.ts', '!**/index.ts', '!**/main.ts'],
  coverageDirectory: 'coverage',
};

export default config;
