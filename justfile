# LibreSearch - Semantic Search Engine

# Start everything: SurrealDB + backend + frontend
up:
    #!/usr/bin/env bash
    set -e
    echo "Starting SurrealDB..."
    docker compose up -d
    sleep 2
    echo "Starting backend..."
    cd backend && ../venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8081 &
    BACKEND_PID=$!
    echo "Starting frontend..."
    cd frontend && npm run dev &
    FRONTEND_PID=$!
    echo ""
    echo "LibreSearch is running:"
    echo "  Frontend:  http://localhost:5173"
    echo "  Backend:   http://localhost:8081"
    echo "  API docs:  http://localhost:8081/docs"
    echo "  SurrealDB: ws://localhost:8000"
    echo ""
    echo "Press Ctrl+C to stop all services"
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; docker compose down; echo 'All services stopped.'" EXIT
    wait

# Stop everything
down:
    #!/usr/bin/env bash
    echo "Stopping backend..."
    fuser -k 8081/tcp 2>/dev/null || true
    echo "Stopping frontend..."
    fuser -k 5173/tcp 2>/dev/null || true
    echo "Stopping SurrealDB..."
    docker compose down
    echo "All services stopped."

# Start only SurrealDB
db:
    docker compose up -d

# Start only backend (assumes SurrealDB is running)
backend:
    cd backend && ../venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8081 --reload

# Start only frontend
frontend:
    cd frontend && npm run dev

# Install all dependencies
install:
    #!/usr/bin/env bash
    set -e
    echo "Creating Python venv..."
    python3 -m venv venv
    echo "Installing Python deps..."
    ./venv/bin/pip install -r backend/requirements.txt
    echo "Installing frontend deps..."
    cd frontend && npm install
    echo "Done!"

# Check status of all services
status:
    #!/usr/bin/env bash
    echo "SurrealDB:"
    docker ps --filter name=surrealdb --format "  {{'{{'}}.Status{{'}}'}}" || echo "  not running"
    echo "Backend (port 8081):"
    fuser 8081/tcp 2>/dev/null && echo "  running" || echo "  not running"
    echo "Frontend (port 5173):"
    fuser 5173/tcp 2>/dev/null && echo "  running" || echo "  not running"

# Reset database (destructive)
reset-db:
    #!/usr/bin/env bash
    echo "This will delete ALL data. Press Enter to confirm or Ctrl+C to cancel."
    read
    docker compose down
    rm -rf data
    docker compose up -d
    echo "Database reset."
