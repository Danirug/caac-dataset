module.exports = {
  forbidden: [
    {
      name: 'R01-domain-no-infrastructure',
      severity: 'error',
      from: { path: '^src/domain/' },
      to: { path: '^src/infrastructure/' },
    },
    {
      name: 'R02-domain-no-application',
      severity: 'error',
      from: { path: '^src/domain/' },
      to: { path: '^src/application/' },
    },
    {
      name: 'R03-application-no-presentation',
      severity: 'error',
      from: { path: '^src/application/' },
      to: { path: '^src/infrastructure/http/' },
    },
    {
      name: 'R05-domain-no-listed-frameworks',
      severity: 'error',
      from: { path: '^src/domain/' },
      to: {
        path:
          '(^|/)(node_modules/)?' +
          '(fastify|@fastify/swagger|@fastify/swagger-ui)(/|$)',
      },
    },
    {
      name: 'R06-inner-no-postgres-client',
      severity: 'error',
      from: { path: '^src/(domain|application)/' },
      to: {
        path: '(^|/)(node_modules/)?pg(/|$)',
      },
    },
    {
      name: 'unresolved-imports',
      severity: 'error',
      from: {},
      to: { couldNotResolve: true },
    },
  ],

  options: {
    doNotFollow: {
      path: 'node_modules',
    },
    tsPreCompilationDeps: true,
    tsConfig: {
      fileName: 'tsconfig.json',
    },
  },
};