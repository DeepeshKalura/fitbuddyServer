# Fitbuddy Backend

Fitbuddy is a project that aims for users to achieve physical and mental fitness.

## Features

The main functionality of the Fitbuddy backend includes:

- User management: Create, update, and delete user accounts.
- Post management: Create, update, and delete posts.
- Retrieval endpoints: Retrieve a list of all users or posts, and retrieve specific user or post details by ID.

## Setup

To set up the Fitbuddy backend locally, follow these steps:

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DeepeshKalura/fitbuddyServer
    ```

2. Navigate into the project directory:

    ```bash
    cd fitbuddyServer
    ```

3. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

Once you have installed the dependencies, you can start the backend server by running the following command:

```bash
uvicorn main:app --reload
```

The server will start, and you can access it at `http://localhost:8000`.

## Contributing

We welcome contributions to enhance the Fitbuddy backend! If you'd like to contribute, please follow the guidelines outlined in the CONTRIBUTING.md file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 

