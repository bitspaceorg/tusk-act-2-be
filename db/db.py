import psycopg2
import os


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"]
        )
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def insert(self, domain, route=None):
        self.cur.execute("SELECT id FROM domain WHERE domain = %s;", (domain,))
        domain_result = self.cur.fetchone()

        if not domain_result:
            self.cur.execute(
                "INSERT INTO domain (domain) VALUES (%s) RETURNING id;",
                (domain,)
            )
            domain_id = self.cur.fetchall()[0]
            self.conn.commit()
        else:
            domain_id = domain_result[0]

        if route:
            self.cur.execute(
                "SELECT id FROM routes WHERE domain_id = %s AND routes = %s;",
                (domain_id, route)
            )
            route_result = self.cur.fetchone()

            if not route_result:
                self.cur.execute(
                    "INSERT INTO routes (domain_id, routes) VALUES (%s, %s);",
                    (domain_id, route)
                )
                self.conn.commit()

    def check(self, domain, route=None):
        self.cur.execute("SELECT id FROM domain WHERE domain = %s;", (domain,))
        domain_result = self.cur.fetchone()

        res = {"domain": True, "route": False}

        if not domain_result:
            res["domain"] = False
            return res

        if route:
            domain_id = domain_result[0]
            self.cur.execute(
                "SELECT id FROM routes WHERE domain_id = %s AND routes = %s;",
                (domain_id, route)
            )
            route_result = self.cur.fetchone()
            res["route"] = route_result is not None

        return res
