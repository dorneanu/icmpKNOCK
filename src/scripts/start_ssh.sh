#!/bin/sh

HOST=localhost

keys='c7533ff6fabc19816a2d816941fa5f56
fafe47632b2a5e0a8b5fe2e8406b970b
f28dff849929fb5d43629328c23df1c1
b96276ed3de61330494eb201a3cb7fa7
519ac16ecadcc9b3b1f30a2133d98907'

for k in $keys
do
   ping -c 1 -p $k $HOST
done
