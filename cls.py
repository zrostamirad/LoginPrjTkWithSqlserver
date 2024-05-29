from connection import *

curser = connection.cursor()


class Repository():
    def Insert(self, TblName, Key, Val):
        try:
            curser.execute("insert into " + TblName + "(" + Key + ")values(" + Val + ")")
            curser.commit()
            return True
        except:
            return False

    def SelectAll(self, TblName, Key):
        try:
            result = curser.execute("select " + Key + " from " + TblName)
            return result
        except:
            return ()

    def SelectById(self, TblName, Key, where):
        try:
            curser.execute("select " + Key + " from " + TblName + " where " + where)
            result = curser.fetchone()
            return result
        except:
            return ()

    def SelectByFeild(self, TblName, Key, where):
        try:
            curser.execute("select " + Key + " from " + TblName + " where " + where)
            result = curser.fetchall()
            return result
        except:
            return ()

    def Update(self, TBLName, Val, where):
        try:
            curser.execute("update " + TBLName + " set " + Val + " where " + where)
            curser.commit()
            return True
        except:
            return False

    def Delete(self, TBLName, where):
        try:
            curser.execute("delete from " + TBLName + " where " + where)
            curser.commit()
            return True
        except:
            return False

    def Search(self, TblName, Col, where):
        try:
            result = curser.execute("select " + Col + " from " + TblName + " where " + where)
            return result
        except:
            return ()
