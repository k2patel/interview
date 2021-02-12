#!/usr/bin/env python3

import os

file = open(os.getcwd() + '/test_data/01-input', 'r')
lines = file.readlines()

count = 0

for line in lines:
  count = count + int(line)

print(count) 
