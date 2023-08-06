import sqlalchemy as sa
from lr.Models.db import sql_server

class auxDB():
    id = sa.Column(sa.Integer,primary_key=True,autoincrement=True)

    def save(self):
        try:
            if not self.id:
                sql_server.session.add(self)
            sql_server.session.commit()
        except:
            sql_server.session.rollback()
            raise
        
    
    def delete(self):
        sql_server.session.rollback()
        sql_server.session.delete(self)
        sql_server.session.commit()

