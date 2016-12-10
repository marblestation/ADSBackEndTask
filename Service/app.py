from ReferenceResolver import app
from log import setup_logging
setup_logging()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
