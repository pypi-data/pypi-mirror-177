# Copyright (c) 2021 Matteo Redaelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import json
import os
import re
import time
from datetime import date
from datetime import timedelta

def find_changes(qrs, start_time, end_time):
    pFilter = f"modifiedDate ge '{start_time}' and modifiedDate le '{end_time}'"
    logging.debug("Searching dataconnections with pFilter= " + str(pFilter))
    path = "/qrs/dataconnection/full"
    param = {"filter": pFilter} 
    result = qrs.driver.get(path, param).json()
    return result

def find_old_apps(
    qrs,
    modified_days,
    last_reload_days,
    published,
    pFilter,
    target_path,
    save_meta,
    skipdata,
    export,
    delete,
):
    if delete and (modified_days < 60 or last_reload_days < 60):
        logging.error("You want to delete too recent apps. Bye")
        return 1
    apps = get_old_apps(
        qrs, modified_days, last_reload_days, published=published, pFilter=pFilter
    )
    for app in apps:
        logging.debug("Found app: " + str(app))
        resp = False
        if export:
            logging.warning("Removing app: " + app["id"])
            resp = export_app(
                qrs,
                app=app,
                target_path=target_path,
                save_meta=save_meta,
                skipdata=skipdata,
            )

        if delete:
            logging.warning("Removing app: " + app["id"])
            # An app can deleted if and only if it was successuffly exported to a file
            if resp and resp.status_code == 200:
                qrs.AppDelete(app["id"])
            else:
                logging.error("Cannot export (and then delete) app: " + app["id"])
    return apps
