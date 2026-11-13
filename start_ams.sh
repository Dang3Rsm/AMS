#!/bin/bash

echo "Starting MySQL service for AMS..."
sudo systemctl start mysql

# Ensure MySQL is stopped automatically when you press Ctrl+C
trap 'echo -e "\nStopping MySQL service to free up RAM..."; sudo systemctl stop mysql; echo "Done!"; exit 0' SIGINT SIGTERM EXIT

echo "Launching AMS Flask Server on http://localhost:5000 ..."
source .venv/bin/activate
python run.py
