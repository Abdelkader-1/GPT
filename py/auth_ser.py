import Db_authentication
import modelConnection
conn = modelConnection.conn()
conn.set_openai_environment_variables()
auth = Db_authentication.Auth()
auth.read_credentials()
df_dict,table_schema,engine = auth.schema_describtion()
