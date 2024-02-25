# Item Management API for GPTs

This is a simple API to manage items. It is part of a tutorial for custom actions in GPTs.

## Setup

The project is written in Python and uses the FastAPI framework. To set up the project, you need to install the required dependencies. You can do this by running the following command:

```bash
pip install fastapi uvicorn aiosqlite
```

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --reload
```

This will start the server at `http://localhost:8000`.

## API Endpoints

The API has the following endpoints:

### GET /items/{item_id}

This endpoint retrieves an item by its ID. If the item does not exist, it returns a 404 error.

#### Parameters

- `item_id` (path, required): The ID of the item.

#### Responses

- `200 OK`: Returns the item.
- `404 Not Found`: If the item does not exist.

### POST /items/

This endpoint creates a new item.

#### Request Body

- `item` (body, required): The item to create. It should be a JSON object with the following properties:
  - `name`: The name of the item.
  - `description`: The description of the item.
  - `price`: The price of the item.
  - `tax`: The tax of the item.

#### Responses

- `200 OK`: Returns the created item.

## Authentication

The API uses API key authentication. The API key should be sent in the `Authorization` header in the format `Bearer {API_KEY}`. The API key is checked in the `get_basic_api_key` function.

## Database

The API uses SQLite for the database. The database operations are performed asynchronously using the `aiosqlite` library. The database schema is defined in the `create_table` function.

## Models

The `Item` model is used to represent items. It has the following properties:

- `name`: The name of the item.
- `description`: The description of the item.
- `price`: The price of the item.
- `tax`: The tax of the item.

To set up ngrok for your FastAPI application, follow these steps:

1. Download ngrok: Visit the [ngrok download page](https://ngrok.com/download) and download the version for your operating system.

2. Unzip the downloaded file: This will create a new file called `ngrok` (or `ngrok.exe` on Windows).

3. Connect your account: Run the command `./ngrok authtoken YOUR_AUTH_TOKEN`, replacing `YOUR_AUTH_TOKEN` with the auth token from your ngrok account. You can find this token on your [ngrok dashboard](https://dashboard.ngrok.com/get-started/setup).

4. Start an HTTP tunnel: Run the command `./ngrok http 8000` to start a new HTTP tunnel on port 8000, which is the port your FastAPI application is running on.

After running these commands, ngrok will provide a URL that you can use to access your FastAPI application from anywhere. This URL will look something like `http://12345678.ngrok.io`.

Please note that the free version of ngrok provides a random URL every time you start a tunnel. If you need a stable URL, you'll need to upgrade to a paid ngrok plan.