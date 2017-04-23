from spark.Helpers import env
from spark import app

# Boot up app
if __name__ == "__main__":
  app.run(debug=(env == 'development'))
