# backend-fastapi

## Setup and run

### Develop

1. **Clone the repository**
   ```bash
   git clone https://github.com/PrettyPet-Organization/backend-fastapi.git
   cd backend-fastapi
   git checkout develop
   ```
2. **Rename the [`.env.template`](.env.template) file to `.env`**, configure it

3. **Run**
   easy way
   ```bash
   DOTENV_MODE=true uvicorn main:app
   ```
   from root dir

   **Docker**
    ```bash
    make docker-run
    ```
    if Dockerfile was changed:
    ```bash
    docker-run-build
    ```

#### Access points
* Service will be available at `http://localhost:8000`
* Swagger: `http://localhost:8000/docs#/`
