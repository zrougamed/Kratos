# Project: Kratos ⚓

Kratos (named after the Greek personification of strength and power) is a Python-based script for managing Docker containers and stacks via the Portainer API. This tool provides robust features to streamline container orchestration and stack management.

## Features 🔐

- **Authenticate**: Securely authenticate with the Portainer API.
- **Container Management**: Start containers and fetch logs effortlessly.
- **Stack Creation**: Deploy new stacks using Docker Compose content.
- **Stack Insights**: Retrieve detailed information about stacks and their containers.
- **Notification System Integration**: Notify users with container logs via external systems.

## Prerequisites ⏳

- Python 3.x
- `requests` library

Install dependencies with:

```bash
pip install requests
```

## Usage ⚖️

1. **Configuration**:
   Update the placeholders in the script:
   - `PORTAINER_URL`: The URL of your Portainer instance.
   - `USERNAME`: Your Portainer username.
   - `PASSWORD`: Your Portainer password.
   - `ENDPOINT_ID`: The ID of the Portainer endpoint to target.

2. **Run the script**:

```bash
python kratos.py
```

## Example Workflow 🐈

1. **Authenticate**:
   Retrieve a JWT token to interact with the Portainer API.

2. **View Stacks**:
   Get details of all available stacks in the Portainer instance.

3. **Container Logs**:
   Fetch logs for containers and send them as notifications.

4. **Create New Stack**:
   Deploy a new stack directly from a Docker Compose file.

## Example Docker Compose Content 🛠

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "1212:80"
```

## Debugging 🔧

Enable debug mode by setting `DEBUG = True` in the script. This will print JWT tokens, logs, and other useful information for troubleshooting.

## Integration with Notification System 📢

Enhance the script by integrating with the [dynamic-notification-system](https://github.com/zrougamed/dynamic-notification-system). Example payload:

```python
payload = {
    "notification_type": "ntfy",
    "message": {
        "title": subject,
        "message": message,
    },
}
requests.post("http://localhost:8080/notify", data=json.dumps(payload))
```

## Contribution 🌎

Contributions are welcome! Feel free to submit issues or pull requests to improve the script.

## License ©

Kratos is licensed under the MIT License.
