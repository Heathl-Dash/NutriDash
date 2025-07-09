#!/bin/bash
python app/tasks/consumer.py &

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload