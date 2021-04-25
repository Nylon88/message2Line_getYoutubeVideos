import sqlite3


class Database:
    #テーブルが存在していない場合は以下を実行する
    CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS global_flag
    (user_id  primary key ,
    inputText_bool )'''
    conn = sqlite3.connect('testdb.sqlite3')
    c = conn.cursor()
    c.execute(CREATE_TABLE)
    conn.commit()
    
    def insert(self, user_id, inputText_bool) -> str:
        TEST_INSERT = '''INSERT INTO global_flag (user_id, inputText_bool)
        VALUES (?, ?)
        '''
        data = (user_id, inputText_bool)
        try:
            Database.c.execute(TEST_INSERT, data)
            Database.conn.commit()
            # conn.close()
            return 'seccess'
        except Exception as e:
            print(f'error insert: {e}')

    def get_data(self, user_id) -> tuple:
        TEST_SELECT = "SELECT * FROM global_flag WHERE user_id=?"
        data = (user_id,)

        try:
            result = Database.c.execute(TEST_SELECT, data).fetchone()
            if result == None:
                result = (False, False)
                return result

            return result

        except Exception as e:
            print(f'error get_data: {e}')

    def update(self, user_id, inputText_bool) -> str:
        TEST_UPDATE = "UPDATE global_flag SET inputText_bool=? WHERE user_id=?"
        data = (inputText_bool, user_id)

        try:
            Database.c.execute(TEST_UPDATE, data)
            Database.conn.commit()
            return 'seccess'
        except Exception as e:
            print(f'error update: {e}')

    def conf_userId_inputText_bool(self, user_id) -> tuple:

        """
            ②user_idが登録されているかの検証
            ①その結果とuser_idが登録されていればinputText_boolの値を返す
        """

        result = self.get_data(user_id=user_id) 
        # データベース内にuser_idが登録されていない場合
        if result[0] is False:
            return ('user_idが登録されていませんでした', False)

        # データベース内にuser_idが登録されているinputText_boolの値を返す
        return ('user_idが登録されています', result[1])

    def get_inputText_bool(self, user_id) -> bool:

        """
            ①user_idが登録されていないときの処理
            ②inputText_boolの値を返す
        """

        result = self.conf_userId_inputText_bool(user_id=user_id)

        # user_idが登録されていなければ、新規でuser_idを登録する
        if result[0] == 'user_idが登録されていませんでした':
            print('user_idが登録されていませんでした')
            self.insert(user_id=user_id, inputText_bool=0)
            return False

        # 戻り値が1ならtrue 0ならfalseに変換する
        if result[1] == 1:
            return True
        return False

    def update_inputText_bool(self, user_id, inputText_bool):
        """
            inputText_boolの値を更新する
        """

        # true→1 false→0として変換する
        if inputText_bool is True:
            self.update(user_id=user_id, inputText_bool=1)
            return 'Success'
        
        self.update(user_id=user_id, inputText_bool=0)
        return 'Success'
        
        


if __name__ == '__main__':
    databese = Database()
    
    #print(databese.insert(user_id='cgj', inputText_bool=True))
    
    #print(databese.get_data('cgj'))
    print(databese.get_inputText_bool('lgv'))
    #print(databese.update_inputText_bool('dlo', False))


    # TEST_SELECT = 'select * from global_flag where user_id = ?'
    # #TEST_SELECT = "SELECT * FROM global_flag WHERE user_id = ?"
    # data = ('1sdghgvv', )
    # c.execute(TEST_SELECT, data)
    # result = c.execute(TEST_SELECT, data)
    # print(result.fetchone())
    # c.close()


