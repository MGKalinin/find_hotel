import sqlalchemy as db

# TODO Fixed by doing pip install --force-reinstall 'sqlalchemy<2.0.0'
#  (в поздних версиях выдаёт ебанутую ошибку)

# создать движок
engine = db.create_engine('sqlite:///hotels.db')
# запуск и подключение
conn = engine.connect()
# метаданные
metadata = db.MetaData()
# таблица, колонки, типы данных
hotels = db.Table('SearchResult', metadata,
                  db.Column('id', db.Integer, primary_key=True),
                  db.Column('name_city', db.Text),
                  db.Column('name_hotel', db.Text),
                  db.Column('min_price', db.Integer),
                  db.Column('max_price', db.Integer),
                  db.Column('check_in_day', db.Text),
                  db.Column('exit_day', db.Text),
                  )

# создать таблицу
# metadata.create_all(engine)

# добавить элементы в базу данных
# make_entry = hotels.insert().values([
#     {'name_city': 'Rome', 'min_price': '110'}])

# запись новых данных
# conn.execute(make_entry)

# select_all_query = db.select([hotels])
# select_all_results = conn.execute(select_all_query)
# print(select_all_results.fetchall())


# if __name__ == '__main__':
