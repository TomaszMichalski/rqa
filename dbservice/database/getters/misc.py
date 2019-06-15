# database.getters.py


def get_address_id_by_coord(cur, latitude, longitude):
    print(
        "Executing query: SELECT address_id FROM addresses"
        " WHERE latitude = '{0}' AND longitude = '{1}';".format(latitude, longitude))
    cur.execute("SELECT address_id FROM addresses WHERE latitude = %s AND longitude = %s;",
                (latitude, longitude))
    address_id = cur.fetchone()
    if address_id is None:
        return None
    return address_id[0]


def get_coordinates_for_each_address(cur):
    print("Executing query: SELECT latitude, longitude FROM addresses;")
    cur.execute("SELECT address_id, latitude, longitude FROM addresses;")
    coordinates = cur.fetchall()
    return coordinates


def get_airly_installation_ids(cur):
    print("Executing query: SELECT installation_id FROM airly_installations")
    cur.execute("SELECT installation_id FROM airly_installations")
    installations = cur.fetchall()
    return installations


def get_airly_installation_by_id(cur, insta_id):
    print("Executing query: SELECT * FROM airly_installations WHERE installation_id = '{0}';".format(insta_id))
    cur.execute("SELECT * FROM airly_installations WHERE installation_id = '%s';", (insta_id,))
    installation = cur.fetchone()
    return installation


def get_address_id_for_installation_id(cur, iid):
    print("Executing query: SELECT address_id FROM airly_installations WHERE installation_id = '{0}';".format(iid))
    cur.execute("SELECT address_id FROM airly_installations WHERE installation_id ='%s';", (iid,))
    address_id = cur.fetchone()
    return address_id