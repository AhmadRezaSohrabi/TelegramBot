from flask_failsafe import failsafe

@failsafe
def initiate_application():
    from app import app
    return app

if __name__ == '__main__':
    initiate_application().run(debug=True, port=80)