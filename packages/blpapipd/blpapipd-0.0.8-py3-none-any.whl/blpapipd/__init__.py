# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 06:24:36 2022

@author: T. Nicolas Steinbach
"""

# module level doc-string
__doc__ = """
blpapipd - access BBG data directly into pandas Series (time) and DataFrames
=====================================================================

Retrieve BBG time-series into manupulable Series and DataFrames for further use
in data analysis, signal generation and plotting

Main Features
-------------
Here are just a few of the things you can do:

  - connect once to BBG DAPI and use many
  - simple query .get() function
  - built in cache, helpful when creating new reports or running through
  same query many times (in development or debugging)
  - queries return pandas time-series, w/ datetime indexes
  
  
"""
