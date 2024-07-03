from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getCountry():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gr.Country 
                from go_retailers gr """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailersOfCountry(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from go_retailers gr 
                where gr.Country = %s"""

        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesoRetailers(anno,u,v):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct gds2.Product_number) as peso
                from go_daily_sales gds1, go_daily_sales gds2 
                where gds2.Product_number = gds1.Product_number and gds2.Retailer_code = %s and gds1.Retailer_code = %s and YEAR(gds1.`Date`)= YEAR(gds2.`Date`) 
                and YEAR(gds2.`Date`)= %s """

        cursor.execute(query, (u,v,anno,))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result
