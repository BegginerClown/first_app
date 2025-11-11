import sqlite3

class DB:

    def __init__(self, db_file: str):
        self.db_file = db_file

    def get_connection(self):
        conn = sqlite3.connect(
            self.db_file,
            check_same_thread=False,
            timeout=10.0,
            isolation_level=None
        )
        conn.row_factory = sqlite3.Row
        return conn

    def get_player_data(self, name: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    select
                    pos_x,
                    pos_y,
                    hunger,
                    happiness,
                    energy
                    from Player_condition
                    where name = ?
                    """, (name,)
                )
                row = cursor.fetchone()

                if row is not None:
                    return {
                        'pos_x': row['pos_x'],
                        'pos_y': row['pos_y'],
                        'hunger': row['hunger'],
                        'happiness': row['happiness'],
                        'energy': row['energy']
                    }
                else:
                    print(f"Игрок с именем '{name}' не найден, создаю нового")
                    self.insert_player_data(name)
                    print(f"Игрок c именем '{name}' создан")
                    return self.get_player_data(name)
            except Exception as ex:
                print(f'Ошибка получении данных об игроке: {ex}')



    def set_player_data(self, pos_x: int, pos_y: int, hunger: int, happiness: int, energy: int, name: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    update Player_condition set
                    pos_x = ?,
                    pos_y = ?,
                    hunger = ?,
                    happiness = ?,
                    energy = ?
                    where name = ?
                    """, (pos_x, pos_y, hunger, happiness, energy, name)
                )
            except Exception as ex:
                print(f'Ошибка получения данных об игроке: {ex}')

    def insert_player_data(self, name: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    insert into Player_condition(name)values(?)
                    """, (name,)
                )
            except Exception as ex:
                print(f'Ошибка при инсерте данных: {ex}')

    def get_all_players(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """select name from Player_condition"""
            )
            rows = cursor.fetchall()
            return [row['name'] for row in rows]

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    CREATE TABLE if not exists Player_condition (
                    Id INTEGER,
                    Pos_x INTEGER DEFAULT (200) NOT NULL,
                    Pos_y INTEGER DEFAULT (500) NOT NULL,
                    Hunger INTEGER DEFAULT (100),
                    Happiness INTEGER DEFAULT (100),
                    Energy INTEGER DEFAULT (100),
                    Name TEXT not null,
                    CONSTRAINT Player_condition_PK PRIMARY KEY (Id)
                    );
                    """
                )
            except Exception as ex:
                print(f'Ошибка пр создании таблицы: {ex}')