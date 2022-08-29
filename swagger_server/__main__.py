#!/usr/bin/env python3

import connexion

from swagger_server import encoder


def main():
    print("Starting app1")
    app = connexion.App(__name__, specification_dir='./swagger/')
    print("Starting app2")
    app.app.json_encoder = encoder.JSONEncoder
    print("Starting app3")
    app.add_api('swagger.yaml', arguments={'title': 'OpenAPI definition'}, pythonic_params=True)
    print("Starting app4")
    app.run(port=8080)


if __name__ == '__main__':
    main()
