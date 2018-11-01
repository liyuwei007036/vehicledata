import pymysql


class mysql:
    def __init__(self):
        self.coon = pymysql.connect("localhost", "root", "123456", "test")
        self.cursor = self.coon.cursor()

    def get_brand(self, che_168_id):
        sql = 'select id, name from VehicleBrand where che168_brand_id = %d' % che_168_id
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def get_series(self, che_168_id):
        sql = 'select id, name from VehicleSeries  where parent_id is not and che168_series_id = %d' % che_168_id
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def get_parent_series(self, che_168_id):
        sql = 'select id, name from VehicleSeries where parent_id is null and che168_series_id = %d' % che_168_id
        self.cursor.execute(sql)
        ret = self.cursor.fetchone()
        return ret

    def get_model(self, che_168_id):
        sql = 'select id, name from VehicleModel where che168_model_id = %d' % che_168_id
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def insert_brand(self, tur):
        sql = 'insert into VehicleBrand (alias, che168_brand_id, initial, name, valid) values (%s, %s, %s ,%s, %s)'
        self.cursor.execute(sql, tur)
        self.coon.commit()
        return self.cursor.lastrowid

    def insert_parent_series(self, tur):
        sql = 'INSERT INTO VehicleSeries (name, alias, che168_series_id, valid, brand_name, brand_id, sort_order) ' \
              'VALUES(%s, %s, %d, %s, %s, %d, %d)'
        self.cursor.execute(sql, tur)
        self.coon.commit()
        return self.cursor.lastrowid

    def insert_child_series(self, ls=[]):
        sql = 'INSERT INTO VehicleSeries (name, alias, che168_series_id, valid,  brand_name, brand_id , sort_order, parent_id, status)' \
              'VALUES(%s, %s, %d, %s, %s, %d, %d, %d, %s)'
        self.cursor.executemany(sql, ls)
        self.coon.commit()

    def insert_model(self, tur):
        sql = 'INSERT INTO VehicleModel (name, alias, che168_model_id, valid, brand_name, brand_id, series_id, series_name, body_type, gearbox, engine, structure, drive_mode, seat)' \
              'VALUES(%s, %s, %d, %s, %s, %d, %d, %s, %s, %s, %s, %s, %s, %d)'
        self.cursor.execute(sql, tur)
        self.coon.commit()

    def insert_model_detail(self, ls=[]):
        sql = 'INSERT INTO VehicleModelData (model_id, type, property, is_number, string_value, number_value)' \
              ' VALUES(%d, %s, %s, %d, %s, %d)'
        self.cursor.executemany(sql, ls)
        self.coon.commit()
