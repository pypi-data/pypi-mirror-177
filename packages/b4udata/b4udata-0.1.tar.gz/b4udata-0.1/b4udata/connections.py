from sqlalchemy import create_engine

class Database():

    def __init__(self,user,password,host,port,databasename):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.databasename = databasename

    def connect(self):
        return create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                self.user, self.password, self.host, self.port,self.databasename
            )
        )