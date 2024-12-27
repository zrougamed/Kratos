"""
This script interacts with the Portainer API to manage Docker containers and stacks. It provides functionalities such as:

1. Authenticating with the Portainer API.
2. Starting containers by their IDs.
3. Fetching and sending container logs.
4. Creating new stacks from Docker Compose content.
5. Fetching details about stacks and containers.
6. Sending notifications using an external notification system.

Functions:
- `authenticate()`: Authenticates with the Portainer API and returns a JWT token.
- `start_container(jwt_token, container_id)`: Starts a Docker container using its ID.
- `fetch_logs(jwt_token, container_id)`: Retrieves logs for a specified container.
- `send_notification(subject, message)`: Sends notifications (e.g., using the dynamic-notification-system).
- `create_container_from_compose(jwt_token, compose_file_content)`: Creates a new stack from Docker Compose content.
- `get_stacks(jwt_token)`: Fetches all stacks in the Portainer instance.
- `get_stack_containers(jwt_token, stack_id)`: Fetches all containers in a specific stack.

Main Scheduler:
- Authenticates with the API.
- Retrieves and prints information about all stacks and their containers.
- Optionally starts containers and fetches logs.
- Creates a new stack and retrieves details about its containers.

Dependencies:
- `requests`: For making HTTP requests to the API.
- `json`: For handling JSON payloads.
- `time`: For adding delays during container startup.

Note:
Replace placeholders like `PORTAINER_URL`, `USERNAME`, `PASSWORD`, and `ENDPOINT_ID` with actual values.
"""
import requests
import time
import json 

# DEBUG var ( turn off in Production )
DEBUG = True 

# Portainer API details
PORTAINER_URL = "http://your-portainer-instance:9000/api"   # change this
USERNAME = "admin"                                          # change this
PASSWORD = "password"                                       # change this

# get the endpoints here:
# http://your-portainer-instance:9000/api/endpoints
# for example Master Portainer ID 1
ENDPOINT_ID=1                                               # change this

# Authenticate with Portainer
def authenticate():
    """
    Authenticates with the Portainer API and returns a JWT token.

    Returns:
        str: JWT token for further API requests.
    """
    url = f"{PORTAINER_URL}/auth"
    payload = {"Username": USERNAME, "Password": PASSWORD}
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()["jwt"]

# Schedule a container to start
def start_container(jwt_token, container_id):
    """
    Starts a Docker container by its ID.

    Args:
        jwt_token (str): JWT token for authorization.
        container_id (str): ID of the container to start.
    """
    url = f"{PORTAINER_URL}/endpoints/{ENDPOINT_ID}/docker/containers/{container_id}/start"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    print(f"Container {container_id} started successfully.")

# Fetch container logs
def fetch_logs(jwt_token, container_id):
    """
    Retrieves logs for a specified container.

    Args:
        jwt_token (str): JWT token for authorization.
        container_id (str): ID of the container whose logs are to be fetched.

    Returns:
        str: Logs from the container.
    """
    url = f"{PORTAINER_URL}/endpoints/{ENDPOINT_ID}/docker/containers/{container_id}/logs?stdout=true&stderr=true"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Send a notification
def send_notification(subject, message):
    """
    Sends notifications using an external system.

    Args:
        subject (str): Subject of the notification.
        message (str): Message content of the notification.
    """
    # use dynamic-notification-system here :)
    # https://github.com/zrougamed/dynamic-notification-system
    # payload = {
    #     "notification_type":"ntfy",
    #     "message":{
    #         "title": subject,
    #         "message": message,
    #         },
    # }
    # requests.post("http://localhost:8080/notify",data=json.dumps(payload))
    pass 

# Create a container 
# https://docs.portainer.io/api/examples#create-a-container
def create_container_from_compose(jwt_token, compose_file_content):
    """
    Creates a new stack from Docker Compose content.

    Args:
        jwt_token (str): JWT token for authorization.
        compose_file_content (str): Docker Compose file content as a string.

    Returns:
        str: Name of the created stack if successful, None otherwise.
    """
    url = f"{PORTAINER_URL}/stacks?type=2&method=string&endpointId={ENDPOINT_ID}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": "job-stack",  # Replace with your job stack 
        "stackFileContent": compose_file_content
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200 or response.status_code == 201:
        print("Container created successfully.")
        return response.json()["Name"]
    else:
        print(f"Failed to create container: {response.text}")
        return None

# Fetch all stacks
def get_stacks(jwt_token):
    """
    Fetches all stacks in the Portainer instance.

    Args:
        jwt_token (str): JWT token for authorization.

    Returns:
        list: List of stacks in the Portainer instance.
    """
    url = f"{PORTAINER_URL}/stacks"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Get containers in a stack
def get_stack_containers(jwt_token, stack_id):
    """
    Fetches all containers in a specific stack.

    Args:
        jwt_token (str): JWT token for authorization.
        stack_id (str): ID of the stack.

    Returns:
        list: List of containers in the stack.
    """
    url = f"{PORTAINER_URL}/endpoints/{ENDPOINT_ID}/docker/containers/json?filters={{\"label\": [\"com.docker.compose.project={stack_id}\"]}}"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    print(url)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Main scheduler
if __name__ == "__main__":
    try:
        # Authenticate and get JWT token
        jwt_token = authenticate()

        if DEBUG:
            print(jwt_token)
        
        # Fetch all stacks to identify the stack ID
        stacks = get_stacks(jwt_token)

        for stack in stacks:
            print(f"ID: {stack['Id']}, Name: {stack['Name']}")
            stack_id = stack['Name']
            # Fetch containers in the selected stack
            containers = get_stack_containers(jwt_token, stack_id)

            for container in containers:
                print(f"ID: {container['Id']}, Name: {container['Names'][0]}, Image: {container['Image']}")

                container_id = container['Id']
                
                # Start the container
                # start_container(jwt_token, container_id)

                # Wait for the container to initialize
                # time.sleep(10)  # Adjust the sleep time based on your container's startup time

                # Fetch logs
                logs = fetch_logs(jwt_token, container_id)

                if DEBUG:
                    print(logs)

                # Send logs via notification
                send_notification(
                    subject=f"Logs for container {container_id}",
                    message=logs
                )


        ## Create a New Container Stack via the API 
        # Example Docker Compose file content
        docker_compose_content = """
services:
  web:
    image: nginx:latest
    ports:
      - "1212:80"
    """

        # Create the container
        stack_id = create_container_from_compose(jwt_token, docker_compose_content)
        if stack_id is not None:
            print(f"ID: {stack['Id']}, Name: {stack['Name']}")
            
            # Fetch containers in the selected stack
            containers = get_stack_containers(jwt_token, stack_id)

            for container in containers:
                print(f"ID: {container['Id']}, Name: {container['Names'][0]}, Image: {container['Image']}")

                container_id = container['Id']
                
                logs = fetch_logs(jwt_token, container_id)

                if DEBUG:
                    print(logs)

                # Send logs via notification
                send_notification(
                    subject=f"Logs for container {container_id}",
                    message=logs
                )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
