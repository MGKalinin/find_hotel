from peewee import *
from datetime import datetime

db = SqliteDatabase('hotel.db')


class BaseModel(Model):
    class Meta:
        database = db


class MainHotel(BaseModel):
    class Meta:
        db_table = 'hotels'

    # user_id = PrimaryKeyField()
    city = CharField()
    # hotel_name = CharField()
    # min_price = FloatField()
    # max_price = FloatField()
    # check_in_day=
    # check_in_mon=
    # check_in_year=
    # exit_day=
    # exit_mon=
    # exit_year=


# if __name__ == '__main__':
#     db.create_tables([MainHotel])
