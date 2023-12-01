#!/bin/bash

set -xe

mkdir "$1/"
touch "$1/s.py"
touch "$1/ex.txt"
touch "$1/in.txt"
echo "ge $1/*"
