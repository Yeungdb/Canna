from spark.Helpers import env, start_ngrok
from spark import app

is_dev = (env == 'development')

# If in development
# - output ngrok address
# - launch ngrok address in browser
if is_dev:
  start_ngrok()

# Boot up app
if __name__ == "__main__":
  app.run(debug=is_dev)
