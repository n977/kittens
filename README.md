# Kittens API

A REST API revolving around kittens. It features the password OAuth2 flow, as well as architectural patterns such as the repositiory pattern.

Stack:

- FastAPI
- SQLAlchemy
- PostgreSQL
- PyJWT
- Passlib
- Docker

## Interface

The public API interface consists of common CRUD endpoints prefixed with:

- `/v1/colors`
- `/v1/breeds`
- `/v1/kittens`
- `/v1/auth`

Writing data requires authentication through the password OAuth2 flow at `/v1/auth/login`. To create a user, see Development section.

### Examples

[HTTPie](https://github.com/httpie/cli) will be used for demonstration purposes.

Retrieve all kittens:

```sh
http :8000/v1/kittens/
HTTP/1.1 200 OK
content-length: 835
content-type: application/json
date: Fri, 04 Oct 2024 17:08:06 GMT
server: uvicorn

[
    {
        "age": 5,
        "breed_id": "ff494858-36b3-49ab-b7ec-6712f37825af",
        "color_id": "5ce8134a-87e3-4c64-a76d-140ccd2432ec",
        "created_at": "2024-10-04T16:36:26.049422",
        "description": "A British Shorthair kitten",
        "id": "06c7f7e7-4cc8-49b6-8bf3-23277d79336c",
        "updated_at": "2024-10-04T16:36:26.049422"
    },
    {
        "age": 9,
        "breed_id": "c09817ef-c24d-4344-a012-bb1f705a85a8",
        "color_id": "2fa1e68d-a2a9-4f40-9752-68640ab91ffc",
        "created_at": "2024-10-04T16:36:26.049422",
        "description": "A Scottish Fold kitten",
        "id": "1cb50ec8-d27e-4785-9e75-46ee1c337c88",
        "updated_at": "2024-10-04T16:36:26.049422"
    }
]
```

Filter kittens by `breed_id`:

```sh
http :8000/v1/kittens/ breed_id==ff494858-36b3-49ab-b7ec-6712f37825af
HTTP/1.1 200 OK
content-length: 282
content-type: application/json
date: Fri, 04 Oct 2024 17:16:52 GMT
server: uvicorn

[
    {
        "age": 5,
        "breed_id": "ff494858-36b3-49ab-b7ec-6712f37825af",
        "color_id": "5ce8134a-87e3-4c64-a76d-140ccd2432ec",
        "created_at": "2024-10-04T16:36:26.049422",
        "description": "A British Shorthair kitten",
        "id": "06c7f7e7-4cc8-49b6-8bf3-23277d79336c",
        "updated_at": "2024-10-04T16:36:26.049422"
    }
]
```

Log in:

```sh
http POST :8000/v1/auth/login username=user password=password --form
HTTP/1.1 200 OK
content-length: 537
content-type: application/json
date: Fri, 04 Oct 2024 17:31:21 GMT
server: uvicorn

{
    "access_token": "{access_token}",
    "token_type": "Bearer"
}
```

Write data with the acquired token (replace `{access_token}` with your token):

```sh
http POST :8000/v1/kittens/ color_id=5ce8134a-87e3-4c64-a76d-140ccd2432ec age=3 breed_id=ff494858-36b3-49ab-b7ec-6712f37825af description="Another British Shorthair kitten" Authorization:Bearer\ {access_token}
HTTP/1.1 201 Created
content-length: 4
content-type: application/json
date: Fri, 04 Oct 2024 17:39:45 GMT
server: uvicorn

null
```

## Development

The default environment configuration is tailored towards Docker development. Before proceeding, make sure you have `docker` and `docker-compose` installed on your host.

To develop locally, first clone this repository:

```sh
git clone https://github.com/n977/kittens
```

Install dependencies:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

To configure different environments, you may use `.env*`. Default templates are provided as `.env*.example`. Some variable values are ommited and must be filled before continuing further.

### Database

Run the database container:

```sh
docker compose up db -d
```

Run database migrations with `alembic`. To connect to the database container from your host, overwrite `DB_HOST`:

```sh
DB_HOST=127.0.0.1 alembic upgrade head
```

You should now have a complete database, although empty.

#### Seeding

There is a script `scripts/seed.py` which provides initial data to the database to play with. For each table, there is a corresponding file in the `.csv` format under the `csv` directory, so you may edit it.

Seed the database:

```sh
DB_HOST=127.0.0.1 python scripts/seed.py
```

You're required to provide at least one user during this step to authenticate against the API later. There is no registration mechanism exposed in the public interface since only administrators are supposed to have write permissions.

### API

The API server utilizes RSA-256 for authentication purposes, which means that you must generate a PEM key before proceeding. To generate it locally, you may use `openssl`:

```sh
mkdir secrets
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out secrets/private.pem
```

Extract the public key:

```sh
openssl rsa -pubout -in secrets/private.pem -out secrets/public.pem
```

Do not expose the private key. At runtime, both keys will be sourced from the environment by their paths: `KEY_PRIVATE_PATH` and `KEY_PUBLIC_PATH` respectively.

Run the API container:

```sh
docker compose up api -d
```

You should now have a complete development setup.

### Testing

To run tests against a test database, run the database container in a test environment:

```sh
docker compose --env-file .env.test run -P --rm db
```

Run tests with `pytest`:

```sh
DB_HOST=127.0.0.1 pytest tests
```

## Documentation

OpenAPI HTML documentation is available both [online](https://n977.github.io/kittens) and locally through `REDOC_URL` endpoint.
