import mysql.connector


class ShowQuery:
    def __init__(self, *lines):
        self.lines = lines
        print(self.__str__())

    def __str__(self):
        query = "\nMySQL Query Generated:\n"
        for line in self.lines:
            query += line + '\n'
        return query + "--------------------\n"


class Database:
    def __init__(self, use_database='', password='', host='localhost', user='root', overwrite=False):
        self.host = host
        self.user = user
        self.use_database = use_database

        connection_dict = {
            'host': self.host,
            'user': self.user,
            'passwd': password,
        }
        self.mydb = mysql.connector.connect(**connection_dict)
        self.cursor = self.mydb.cursor(dictionary=True)

        if overwrite:
            self.__remove_database(self.use_database)
        self.__create_database(self.use_database)
        use_command = "USE {};".format(self.use_database)
        self.cursor.execute(use_command)
        print("Connection achieved. Using database {}.".format(self.use_database))

    def __str__(self):
        return 'User \'{}\' connected at \'{}\', using database \'{}\'.'.format(
            self.user, self.host, self.use_database
        )

    def __create_database(self, name, show_query=False, sq=False):
        create_command = "CREATE DATABASE IF NOT EXISTS {};".format(name)
        self.use_database = name
        self.cursor.execute(create_command)
        if show_query or sq:
            ShowQuery(create_command, self.use_command)

    def __remove_database(self, name, show_query=False):
        remove_command = "DROP DATABASE {};".format(name)
        self.cursor.execute(remove_command)
        if show_query:
            ShowQuery(remove_command)

    def create_table(self, table_name, column_dict={}, show_query=False, sq=False, **kwargs):
        self.cursor.execute("USE {};".format(self.use_database))
        column_dict.update(kwargs)
        create_command = "CREATE TABLE IF NOT EXISTS {} (\n".format(table_name)
        for column_name, column_type in column_dict.items():
            create_command += "{} {},\n".format(column_name, column_type)
        create_command = create_command.strip(',\n')
        create_command += "\n);"
        if show_query or sq:
            ShowQuery(create_command)
        self.cursor.execute(create_command)


    def show_tables(self, table_name='', all=False, show_query=False, sq=False):
        # TODO single table viewing
        show_command = 'SHOW TABLES;'
        self.cursor.execute(show_command)
        if show_query or sq:
            ShowQuery(show_command)
        for table in self.cursor:
            print(table)

    def execute(self, command):
        cursor = self.mydb.cursor()
        return cursor.execute(command)


db = Database(use_database='testdb', password='Ap069RoX')
db.create_table('test2', x='int', y='int', sq=True)
db.show_tables()
print(db)
