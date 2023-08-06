from datetime import datetime


class ExecuteRebuild:

    def handle(weekday: int, tablename, conn):
        dt = datetime.now().weekday()
        if dt == weekday:
            conn.session.execute("SET NOCOUNT ON; EXEC PR_INDEX :p1", {"p1": tablename})
            conn.session.commit()