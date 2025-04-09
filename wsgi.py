from flaskr import create_app

if __name__ == "__main__":
    app = create_app()
    if app.database_service.active == True:
        app.run(host='appx', port=5000)
    else:
        print("Database not running or is having errors shutting down!")
