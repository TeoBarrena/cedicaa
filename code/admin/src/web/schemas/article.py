from marshmallow import Schema, fields

class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    summary = fields.Str(dump_only=True)
    content = fields.Str(dump_only=True)
    published_at = fields.DateTime(dump_only=True, attribute="publication_date")
    updated_at = fields.DateTime(dump_only=True, attribute="update_date")
    author = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    

class ArticleListSchema(Schema):
    data = fields.List(fields.Nested(ArticleSchema), dump_only=True) #aca con el Nested anida con la clase ArticleSchema y en este caso como no tiene nada de only ni nada, agarra todos los atributos de ArticleSchema
    page = fields.Int(dump_only=True)
    per_page = fields.Int(dump_only=True)
    total = fields.Int(dump_only=True)


#estos son los campos que le va a deovlver en formato json, dps le suma los atributos page, per_page, total
article_schema = ArticleSchema()
#dump_only=True -> significa que solo se utilizarán para la salida de datos (serializacion)