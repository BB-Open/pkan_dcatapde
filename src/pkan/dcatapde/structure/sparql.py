# -*- coding: utf-8 -*-
"""Helpers for SPQRQL"""

# Give me the object to given subject and predicate
# "Attribute" query
WHERE_SP_QUERY = """SELECT DISTINCT ?o
       WHERE {{
          {s} {p} ?o .
       }}"""

# Give me the objects to given predicate
# "a" query
WHERE_P_QUERY = """SELECT DISTINCT ?s
       WHERE {{
          ?s a {p} .
       }}"""
