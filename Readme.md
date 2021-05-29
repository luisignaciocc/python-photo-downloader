# Python Download Script

Script build to download data from a flaky API.

## Objetive

This is a take-home interview for HomeVision that focuses primarily on writing clean code that accomplishes a very practical task.

Given a simple pagianted API hosted at [http://app-homevision-staging.herokuapp.com/api_project/houses?page=1](http://app-homevision-staging.herokuapp.com/api_project/houses?page=1) that returns a list of houses along with some metadata. The task is to write a script that accomplishes the following tasks:

1. Requests the first 10 pages of results from the API
2. Parses the JSON returned by the API
3. Downloads the photo for each house and saves it in a file with the format: `id-[NNN]-[address].[ext]`

There are a few gotchas to watch out for:

1. This is a _flaky_ API! That means that it will likely fail with a non-200 response code. The code _must_ handle these errors correctly so that all photos are downloaded
2. Downloading photos is slow so please think a bit about how you would optimize your downloads, making use of concurrency

## Usage

### With Docker Compose

On the project root

```bash
docker-compose up
```

### Without Docker

You'll need to create and activate a new python3.6 virtual enviroment and configure the respective Mongo database connection on the config.yml file.

```bash
pip install -r requirements.txt
```

```bash
python3.6 start.py
```

#### After execution, the data will be parsed in the database and the photos downloaded in a directory in the project root.

## License

[MIT](https://choosealicense.com/licenses/mit/)
