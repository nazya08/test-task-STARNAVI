# STARNAVI Test Assignment

## Installation and Usage with Docker

Here's how to get the project up and running using docker and docker compose.

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:nazya08/test-task-STARNAVI.git
    ```

2. Copy .env file and fill environment variables
   ```
   cp .env.example .env
   ```
3. Build docker images:
   ```
   docker compose build
   ```
4. Run docker images
   ```
   docker compose up
   ```

Your application should now be running at `http://localhost:8000`

### Create a superuser

To create a superuser you need to connect to the docker container and run the script:
   ```
   docker exec -it tz-starnavi-web-1 python -m src.scripts.superuser <email> <password> <username>
   ```

## Installation and Usage without Docker

Here's how to get the project up and running on your local machine for development and testing.

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:nazya08/test-task-STARNAVI.git
    ```

2. Create virtual env.

    ```
    python -m venv venv
    ```

3. Activate virtual env.

   on Windows:

   ```
   cd venv/Scripts
   ```

   ```
   ./activate
   ```

   on Linux or Mac:

   ```
   source venv/bin/activate
   ```

4. Install requirements:

   ```
   pip install -r requirements.txt
   ```   

5. Run a project:

   ```
   python -m src.main.main
   ```

## Licence

MIT License

Created by Nazar Filoniuk, email: filoniuk.nazar.dev@gmail.com
