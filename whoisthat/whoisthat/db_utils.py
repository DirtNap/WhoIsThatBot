from django.db import models

@models.CharField.register_lookup
class IsEmptyLookup(models.Lookup):

    lookup_name = 'is_empty'
    prepare_rhs = False

    def as_sql(self, compiler, connection):
        if not isinstance(self.rhs, bool):
            raise ValueError('The QuerySet value for an isempty lookup must be True or False')
        sql, params = self.process_lhs(compiler, connection)

        if self.rhs:
            return "({col} IS NULL OR {col} = '')".format(col=sql), params
        else:
            return "({col} IS NOT NULL AND {col} <> '')".format(col=sql), params
