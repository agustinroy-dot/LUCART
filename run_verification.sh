#!/bin/bash
export FLASK_APP=run.py
export FLASK_CONFIG=development
# Seed data
python setup_verification_data.py

# Start server
flask run > flask.log 2>&1 &
PID=$!
sleep 5

# Run verification
python verify_feature.py

# Kill server
kill $PID
