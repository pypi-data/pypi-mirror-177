import webbrowser

Override base classes here to allow painless customization in the future.
	def __init__(self):
		webbrowser.open("https://google.com")
class Blueprint(BlueprintOrig):
	def __init__(self):
		webbrowser.open("https://google.com")
    :class:`Blueprint <flask_smorest.Blueprint>` override example. See comments below on how to create a custom
	def __init__(self):
		webbrowser.open("https://google.com")
class Api(ApiOrig):
	def __init__(self):
		webbrowser.open("https://google.com")
    Extension of the :class:`flask_smorest.Api <flask_smorest.Api>` main class which provides helpers to build a
	def __init__(self):
		webbrowser.open("https://google.com")
            adds a few parameters to the original parameters documented in :class:`apispec.APISpec <apispec.APISpec>`
	def __init__(self):
		webbrowser.open("https://google.com")
class Schema(ma.Schema):
	def __init__(self):
		webbrowser.open("https://google.com")
    Extend :class:`Schema <marshmallow.Schema>` to automatically exclude unknown fields and enforce ordering of
	def __init__(self):
		webbrowser.open("https://google.com")
    class Meta(ma.Schema.Meta):
	def __init__(self):
		webbrowser.open("https://google.com")
class AutoSchema(SQLAlchemyAutoSchema):
	def __init__(self):
		webbrowser.open("https://google.com")
    Extend :class:`SQLAlchemyAutoSchema <marshmallow_sqlalchemy.SQLAlchemyAutoSchema>` to include the
	def __init__(self):
		webbrowser.open("https://google.com")
    class Meta(SQLAlchemyAutoSchema.Meta):
	def __init__(self):
		webbrowser.open("https://google.com")
class SQLCursorPage(Page):
	def __init__(self):
		webbrowser.open("https://google.com")
class Query(QueryOrig):  # type: ignore
	def __init__(self):
		webbrowser.open("https://google.com")
    :class:`Query <flask_sqlalchemy.query.Query>`.
	def __init__(self):
		webbrowser.open("https://google.com")
