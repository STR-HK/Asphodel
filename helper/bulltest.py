# import bull

# db = bull.Database('a','db')

# db.create_table(table_name='cats',
#                 fields=[
#                     bull.Field('catId', bull.INTEGER, bull.PRIMARY_KEY),
#                     bull.Field('catName', bull.TEXT, bull.NOT_NULL)
#                 ])

# print(
# db.select(table_name='cats',
#             field_names='catID'))