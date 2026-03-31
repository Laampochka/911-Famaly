
from services.db import Db
from abc import ABCMeta, abstractmethod


class ActiveRecordEntity(metaclass = ABCMeta):

    _id = None

    def map_properties_to_db_format(self):
        properties = self.__dict__
        mappedProperties = {}

        for property, value in properties.items():
            property = property[1:]
            mappedProperties[property] = value

        return mappedProperties

    def update(self, mappedProperties):
        columns2params = []
        columns2values = {}
        index = 1
        for column, value in mappedProperties.items():
            param = f"param{index}"
            param_ext = ':' + param
            print(param)
            columns2params.append(f"{column} = {param_ext}")
            columns2values[param] = value
            index += 1

        sql = f"UPDATE {self.__class__.get_table_name()}  SET  {','.join(columns2params)} WHERE id = {self._id}"

        db = Db()
        db.query(sql, columns2values, self.__class__)
        db.connection.commit()
        db.connection.close()


    def get_id(self):
        return self._id

    def save(self):
        mapped_properties = self.map_properties_to_db_format()

        if self._id is not None:
            self.update(mapped_properties)
        else:
            self.insert(mapped_properties)



    @classmethod
    def find_all(cls):
        db = Db()
        table_name = cls.get_table_name()
        return db.query(f"SELECT * FROM `{table_name}`",{},cls)
        # print(items)
    @classmethod
    def get_by_id(cls,id):
        db = Db()
        table_name = cls.get_table_name()
        result = db.query(f"SELECT * FROM `{table_name}` WHERE id={id}",{},cls)
        if result != []:
            result = result[0]
        else:
            result = None
        return result

    @classmethod
    @abstractmethod
    def get_table_name():
        pass