# install snowflake-connector-python not snowflake
import snowflake.connector
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import write_pandas


class SnowFlakeConnector():
    
    def __init(self
               , user
               , read_schema = "SCHEMA"
               , write_schema = "WRITE_SCHEMA"
               , warehouse = "WAREHOUSE"
               ):
        self.user = user
        self.password = ""
        self.account = "ACCOUNT"
        self.role = "ROLE"
        self.warehouse = warehouse
        self.database = "DATABASE"
        self.read_schema = read_schema
        self.write_schema = write_schema
        self.authenticator = "externalbrowser"
    
        
    def create_connector(self):
        self.con = snowflake.connector.connect(
            user = self.user
            , password = self.password
            , account = self.account
            , role = self.role
            , warehouse = self.warehouse
            , database = self.database
            , schema = self.read_schema
            , authenticator = self.authenticator
        )
    
        
    def write_df_to_snowflake(self
                              , df
                              , write_schema
                              , table_name
                              , warehouse = "WAREHOUSE"
                              ):
        temp_con = snowflake.connector.connect(
            user = self.user
            , password = self.password
            , account = self.account
            , role = self.role
            , warehouse = warehouse
            , database = self.database
            , schema = write_schema
            , authenticator = self.authenticator
   
        )
        
        success, nchunkg, nrows, _ = write_pandas(temp_con
                                                  , df
                                                  , table_name
                                                  , auto_create_table =  True
                                                  , quote_identifiers = False
                                                 )
        temp_con.close()
        
        if success == 1:
            print(f"Table {table_name} successful created with {str(nrows)} rows!")
        else:
            print("Table not created")
            
class PostgreSQLConnector():
    
    def __init():
        print("connect to Postgres ...")