#!/usr/bin/env python3
# Requires python 3, pymysql
# Login to vault first
# vault login -method=ldap username=<username>

import copy
import json
import subprocess
import sys

import pymysql
from pprint import pprint


def fix_stuff(host, instance):
    with pymysql.connect(
        host=host,
        user=credentials["data"]["user"],
        password=credentials["data"]["password"],
        db="nova",
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f'select flavor from instance_extra where instance_uuid="{instance}"'
            )
            parsed_info = json.loads(cur.fetchone()[0])
            print("Current info in the instance_extra table")
            pprint(parsed_info)
            if (
                parsed_info["cur"]["nova_object.data"]["extra_specs"]["hypervisor"]
                != "shared"
            ):
                parsed_info["cur"]["nova_object.data"]["extra_specs"][
                    "hypervisor"
                ] = "shared"
                new_info = json.dumps(parsed_info)
                print(f"Updating instance {instance}")
                cur.execute(
                    f"update instance_extra set flavor='{new_info}' where instance_uuid=\"{instance}\""
                )
                print(cur._last_executed)
                conn.commit()

def fix_request_specs(host, instahnce):
    print("Checking if we need to fix the request specs")
    with pymysql.connect(
        host=host,
        user=credentials["data"]["user"],
        password=credentials["data"]["password"],
        db="novaapi",
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f'select spec from request_specs where instance_uuid="{instance}"'
            )
            original_specs = json.loads(cur.fetchone()[0])
            print("Current info in the instance_extra table")
            pprint(original_specs)
            if (
                original_specs["nova_object.data"]["flavor"]["nova_object.data"][
                    "extra_specs"
                ]["hypervisor"]
                != "shared"
            ):
                original_specs["nova_object.data"]["flavor"]["nova_object.data"][
                    "extra_specs"
                ]["hypervisor"] = "shared"
                new_info = json.dumps(original_specs)
                print(f"Updating instance {instance}'s extra specs")
                cur.execute(
                    f"update request_specs set spec='{new_info}' where instance_uuid=\"{instance}\""
                )
                print(cur._last_executed)
                conn.commit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage {sys.argv[0]} mysqlhost instasnce_uuid")
        exit(-1)

    credentials = json.loads(
        subprocess.check_output(
            ["vault", "read", "-format", "json", "secret/mysql/nova"]
        )
    )

    fix_stuff(sys.argv[1], sys.argv[2])
    fix_request_specs(sys.argv[1], sys.argv[2])
