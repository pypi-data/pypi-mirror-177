from jija_orm.executors import templates
from jija_orm.executors import executors

table_selector = executors.Executor(
    'pg_catalog.pg_tables',
    templates.Select(name='tablename'),
    templates.Where(
        schemaname__not='pg_catalog\' and schemaname != \'information_schema',
        tablename__not='jija_orm',
        tablename__startswith=executors.Param('app')
    ),
    use_model=False
)

columns_selector = executors.Executor(
    'information_schema.columns',
    templates.Select(
        name='column_name', default='column_default', null='is_nullable',
        type='udt_name', max_length='character_maximum_length'
    ),
    templates.Where(table_name=executors.Param('table')),
    use_model=False
)

migration_id_selector = executors.Executor(
    'jija_orm',
    templates.Select(id='max(id)'),
    use_model=False
)

id_setter = executors.Executor(
    'jija_orm',
    templates.Insert(id=executors.Param('id')),
    use_model=False
)
