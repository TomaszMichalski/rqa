# db_service.py
import json
import airly_reader
import owm_reader


def main():
    """   TODO: add getting data from APIs and sending them to database """

    print(json.dumps(airly_reader.get_measurements(2339), indent=4 ))


if __name__ == "__main__":
    main()
