from flaskr import create_app

app = create_app()  # ← move this out of `__main__` so Gunicorn can find it

if __name__ == "__main__":
    app.run(host='appx', port=5000)

