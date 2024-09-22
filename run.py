import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
