# Make sure all directories have files needed before building Container

# Starting the Application
### 1. Start Podman or Docker Machine
    podman machine start

### 2. Build Podman or Docker container from Containerfile in podman dir
    podman build ./podman 

### 3. Wait some time for Container to build

### 4. Run the Container
    podman run -it <container_id>

### 5. Within another terminal, exec into podman container
    podman exec -it <container_id>


# Using the Application
### 1. First go into frontend and yarn playwright install
    yarn playwright install

### 2. Run frontend app