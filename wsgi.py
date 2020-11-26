import api
import config

if __name__ == "__main__":
    api.run(debug=False, host=config.HOST, port=config.PORT)