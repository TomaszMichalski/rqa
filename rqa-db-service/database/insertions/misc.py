# database.insertions.misc.py
from api import airly_reader
from database.getters import misc


def insert_address(cur, location, address):
    latitude = location.get('latitude')
    longitude = location.get('longitude')
    country = address.get('country')
    city = address.get('city')
    street = address.get('street')
    st_number = address.get('number')

    address_id = misc.get_address_id_by_coord(cur, latitude, longitude)

    if address_id is None:
        print(
            "Executing query: INSERT INTO addresses (latitude, longitude, "
            "country, city, street, st_number) "
            "VALUES ({0}, {1}, {2}, {3},"
            " {4}, {5});".format(latitude, longitude, country, city, street, st_number))
        cur.execute(
            "INSERT INTO addresses (latitude, longitude, "
            "country, city, street, st_number) "
            "VALUES (%s, %s, %s, %s, %s, %s);",
            (latitude, longitude, country, city, street, st_number))

    return misc.get_address_id_by_coord(cur, latitude, longitude)


def insert_nearest_airly_installations(cur, latitude, longitude, *args, **kwargs):
    max_dist = kwargs.get('max_dist', None)
    max_res = kwargs.get('max_res', None)

    installations = airly_reader.get_nearest_installations(latitude, longitude, max_dist=max_dist, max_res=max_res)

    for installation in installations:
        installation_id = installation.get('id')
        if misc.get_airly_installation_by_id(cur, installation_id) is None:
            insert_airly_installation(cur, installation)


def insert_airly_installation(cur, installation_info):
    installation_id = installation_info.get('id')
    location = installation_info.get('location')
    address = installation_info.get('address')

    address_id = insert_address(cur, location, address)

    elevation = installation_info.get('elevation')
    airly = installation_info.get('airly')

    if not misc.get_airly_installation_by_id(cur, installation_id):
        print(
            "Executing query: INSERT INTO airly_installations (installation_id, address_id, elevation, airly)"
            " VALUES ({0}, {1}, {2}, {3});".format(installation_id, address_id, elevation, airly))

        cur.execute("INSERT INTO airly_installations (installation_id, address_id, elevation, airly)"
                    " VALUES (%s, %s, %s, %s);",
                    (installation_id, address_id, elevation, airly))

    return installation_id
