# db_get.py
from logging import Logger


def get_installation_ids(cur):
    print("Executing query: SELECT installation_id FROM installation")
    cur.execute("SELECT installation_id FROM installation")
    installations = cur.fetchall()
    return installations


def get_installation_by_id(cur, insta_id):
    print("Executing query: SELECT * FROM installation WHERE installation_id = '{0}';".format(insta_id))
    cur.execute("SELECT * FROM installation WHERE installation_id = '%s';", (insta_id,))
    installation = cur.fetchone()
    return installation


def get_point_ids(cur):
    print("Executing query: SELECT point_id FROM point")
    cur.execute("SELECT point_id FROM point")
    points = cur.fetchall()
    return points


def get_points(cur):
    print("Executing query: SELECT * FROM point")
    cur.execute("SELECT * FROM point")
    points = cur.fetchall()
    return points


def get_point_id_by_coord(cur, latitude, longitude):
    print("Executing query: SELECT point_id FROM point WHERE latitude"
          " = real {0} AND longitude = real {1}".format(latitude, longitude))
    lat = float(latitude)
    lon = float(longitude)
    cur.execute("SELECT point_id FROM point WHERE latitude = real '%s' AND longitude = real '%s';",
                (lat, lon))
    point = cur.fetchone()
    if point is None:
        return None
    return point[0]


def get_address_id_by_coord(cur, latitude, longitude):
    print(
        "Executing query: SELECT address_id FROM address"
        " WHERE latitude = '{0}' AND longitude = '{1}';".format(latitude, longitude))
    cur.execute("SELECT address_id FROM address WHERE latitude = %s AND longitude = %s;",
                (latitude, longitude))
    address_id = cur.fetchone()
    if address_id is None:
        return None
    return address_id[0]
