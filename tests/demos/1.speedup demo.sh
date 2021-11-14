#!/bin/sh
echo "Here, we're going to run ten sleep 0.1 commands in parallel and then sequentially to compare the runtime."
echo
echo BEGIN_CODE
set -x
parallely sleep1 'sleep 0.1' \
  sleep2 'sleep 0.1' \
  sleep3 'sleep 0.1' \
  sleep4 'sleep 0.1' \
  sleep5 'sleep 0.1' \
  sleep6 'sleep 0.1' \
  sleep7 'sleep 0.1' \
  sleep8 'sleep 0.1' \
  sleep9 'sleep 0.1' \
  sleep0 'sleep 0.1'
echo
parallely --sequential sleep1 'sleep 0.1' \
  sleep2 'sleep 0.1' \
  sleep3 'sleep 0.1' \
  sleep4 'sleep 0.1' \
  sleep5 'sleep 0.1' \
  sleep6 'sleep 0.1' \
  sleep7 'sleep 0.1' \
  sleep8 'sleep 0.1' \
  sleep9 'sleep 0.1' \
  sleep0 'sleep 0.1'
