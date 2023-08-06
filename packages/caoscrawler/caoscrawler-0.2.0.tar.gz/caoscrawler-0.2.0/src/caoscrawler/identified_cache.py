#!/usr/bin/env python3
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2021 Henrik tom Wörden <h.tomwoerden@indiscale.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#


"""
This module is a cache for Records where we checked the existence in a remote server using
identifiables. If the Record was found, this means that we identified the corresponding Record
in the remote server and the ID of the local object can be set.
To prevent querying the server again and again for the same objects, this cache allows storing
Records that were found on a remote server and those that were not (typically in separate caches).
The look up in the cache is done using a hash of a string representation.

TODO: We need a general review:
- How are entities identified with each other?
- What happens if the identification fails?

Checkout how this was done in the old crawler.
"""

import caosdb as db

from hashlib import sha256
from datetime import datetime


def _value_representation(value):
    """returns the string representation of property values to be used in the hash function """

    # TODO: (for review)
    #       This expansion of the hash function was introduced recently
    #       to allow the special case of Files as values of properties.
    #       We need to review the completeness of all the cases here, as the cache
    #       is crucial for correct identification of insertion and updates.
    if value is None:
        return "None"
    elif isinstance(value, db.File):
        return str(value.path)
    elif isinstance(value, db.Entity):
        if value.id is not None:
            return str(value.id)
        else:
            return "PyID="+str(id(value))
    elif isinstance(value, list):
        return "["+", ".join([_value_representation(el) for el in value])+"]"
    elif (isinstance(value, str) or isinstance(value, int) or isinstance(value, float)
          or isinstance(value, datetime)):
        return str(value)
    else:
        raise ValueError(f"Unknown datatype of the value: {value}")


def _create_hashable_string(identifiable: db.Record):
    """
    creates a string from the attributes of an identifiable that can be hashed
    """
    if identifiable.role == "File":
        # Special treatment for files:
        return "P<>N<>{}:{}".format("path", identifiable.path)
    if len(identifiable.parents) != 1:
        # TODO: extend this
        # maybe something like this:
        # parent_names = ",".join(
        #   sorted([p.name for p in identifiable.parents])
        raise RuntimeError("Cache entry can only be generated for entities with 1 parent.")
    rec_string = "P<{}>N<{}>".format(identifiable.parents[0].name, identifiable.name)
    # TODO this structure neglects Properties if multiple exist for the same name
    for pname in sorted([p.name for p in identifiable.properties]):

        rec_string += ("{}:".format(pname) +
                       _value_representation(identifiable.get_property(pname).value))
    return rec_string


def _create_hash(identifiable: db.Record) -> str:
    return sha256(_create_hashable_string(identifiable).encode('utf-8')).hexdigest()


class IdentifiedCache(object):
    def __init__(self):
        self._cache = {}

    def __contains__(self, identifiable: db.Record):
        return _create_hash(identifiable) in self._cache

    def __getitem__(self, identifiable: db.Record):
        return self._cache[_create_hash(identifiable)]

    def add(self, record: db.Record, identifiable: db.Record):
        self._cache[_create_hash(identifiable)] = record
