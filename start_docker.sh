#!/bin/bash
service cron start
yarn --cwd webapp start && python3 main.py