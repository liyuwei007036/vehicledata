import pymysql


class mysql:
    def __init__(self):
        self.coon = pymysql.connect("localhost", "root", "123456", "test")
        self.cursor = self.coon.cursor()

    def get_brand(self, che_168_id):
        sql = 'select id, name from VehicleBrand where che168_brand_id = %s' % che_168_id
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def get_series(self, che_168_id):
        sql = 'select id, name from VehicleSeries where parent_id is not null and che168_series_id = %s' % che_168_id
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def get_parent_series(self, che_168_id):
        sql = 'select id, name from VehicleSeries where parent_id is null and che168_series_id = %s' % che_168_id
        self.cursor.execute(sql)
        ret = self.cursor.fetchone()
        return ret

    def get_model(self, che_168_id):
        sql = 'select id, name from VehicleModel where che168_model_id = %s' % che_168_id
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def insert_brand(self, tur):
        print('*' * 40, '插入品牌', '*' * 40)
        sql = 'insert into VehicleBrand (alias, che168_brand_id, initial, name, valid) values (%s, %s, %s ,%s, %s)'
        self.cursor.execute(sql, tur)
        self.coon.commit()
        return self.cursor.lastrowid

    def insert_parent_series(self, tur):
        print('*' * 40, '插入父车系', '*' * 40)
        sql = 'INSERT INTO VehicleSeries (name, alias, che168_series_id, valid, brand_name, brand_id, sort_order) ' \
              'VALUES(%s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(sql, tur)
        self.coon.commit()
        return self.cursor.lastrowid

    def insert_child_series(self, ls=[]):
        print('*' * 40, '插入子车系', '*' * 40)
        sql = 'INSERT INTO VehicleSeries (name, alias, che168_series_id, valid,  brand_name, brand_id , sort_order, parent_id, status)' \
              'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.cursor.executemany(sql, ls)
        self.coon.commit()

    def insert_model(self, tur):
        print('*' * 40, '插入车型', '*' * 40)
        sql = 'INSERT INTO VehicleModel (name, alias, che168_model_id, valid, brand_name, brand_id, series_id, series_name, body_type, gearbox, engine, structure, drive_mode, seat,emission)' \
              'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(sql, tur)
        self.coon.commit()
        return self.cursor.lastrowid

    def insert_model_detail(self, ls=[]):
        print('*' * 40, '插入车型参数  ---{0}'.format(len(ls)), '*' * 40)
        sql = 'INSERT INTO VehicleModelData (model_id, type, property, is_number, string_value, number_value)' \
              ' VALUES(%s, %s, %s, %s, %s, %s)'
        self.cursor.executemany(sql, ls)
        self.coon.commit()

    def get_series_info(self, series_id):
        sql = 'select id, name, brand_id, brand_name from VehicleSeries where parent_id is not null and che168_series_id = %s' % series_id
        self.cursor.execute(sql)
        return self.cursor.fetchone()
