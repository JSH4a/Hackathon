from app import create_app

if __name__ == "__main__":
    app, socketio = create_app()

    socketio.run(app, host="138.38.198.157",debug=False)

