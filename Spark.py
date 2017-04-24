from spark.Helpers import env, ngrok_address
from spark import app

is_dev = (env == 'development')

# If in development, output ngrok address
if is_dev:
  ngrok_address()

# Boot up app
if __name__ == "__main__":
  app.run(debug=is_dev)
