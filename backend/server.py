from flask import Flask, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os

app = Flask(__name__)
CORS(app)

SUPABASE_URL: str = "https://jnczovwmdeqslohdqjom.supabase.co"
SUPABASE_KEY: str = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpuY3pvdndtZGVxc2xvaGRxam9tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI5OTE2MTAsImV4cCI6MjAyODU2NzYxMH0.jFKLurHSYY7t9dM6sKOkwD3VzlZ-UdPcwWzOj9OSjQQ"
)

db: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/api/logs")
def get_data():
    query = db.table("KEY_LOG").select("*")
    logs = query.execute()
    return jsonify(logs.data)


if __name__ == "__main__":
    app.run()
