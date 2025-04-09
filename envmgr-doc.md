# Docker Environment Manager

This script is designed to simplify the management of Docker environments for developers by abstracting common Docker commands.\
This document provides scenarios and usage examples for the `envmgr.py` script. These scenarios will guide you through common use cases and demonstrate how to effectively utilize the script for managing Docker environments.

## Table of Contents

- [Requirements](#requirements)
- [Environment Setup](#environment-setup)
  - [Debugging](#debugging)
- [Usage](#usage)
  - [Available Commands](#available-commands)
  - [Command Options](#command-options)
- [Environment Variables](#environment-variables)
- [Error Handling](#error-handling)
  - [Example](#example)
- [Scenarios](#scenarios)

## Requirements

- Python 3.x
- Conda-lock
- Docker and Docker Compose
- `.env` file with the necessary environment variables (see [Environment Variables](#environment-variables))

## Environment Setup
In order for the script to work, you must have a locked 
`conda` environment. 

***If you are adding a package in development, make sure it can be installed though `conda-forge`.***

### 1. Install [`conda-lock`](https://conda.github.io/conda-lock/)
```bash
conda install -c conda-forge conda-lock
```

### 2. Lock the Environment
```bash
conda-lock -p linux-64 -f ./environment/stable_env.yml --mamba --kind explicit --filename-template ./environment/stable_env.lock
```

**Explanation:**

- **Platform:** Since Docker is linux native, dependencies must be installed through Linux-64 (and this platform supports a lot of packages).
  - ***make sure dependencies added have linux-64 compatability*** 

- **Mamba flag:** We use a mamba build time image, so to optimize resolves, the mamba flag is used.

- **Kind flag**: Usually conda-lock creates a `.yml`, but this flag allows us to create a `.lock` file instead (for when we create our environment in Docker).

### 3. Development

**DO NOT PUSH CHANGES MADE TO THE DOCKERFILE**

You can test adding dependencies by using the `dev_env.yml` instead of `stable_env.yml` but make sure you **revert** these changes in `Dockerfile_triple`.

- 1. Run this command to lock your `dev_env.yml`:

```bash
conda-lock -p linux-64 -f ./environment/dev_env.yml --mamba --kind explicit --filename-template ./environment/dev_env.lock
```

- 2. Change this line in `Dockerfile_triple` (it's just `stable_env.lock` to `dev_env.lock`):
***Revert this before pushing your changes.***

```bash
RUN --mount=type=bind,source=./environment/dev_env.lock,target=environment.lock \
    --mount=type=cache,target=/opt/conda/pkgs \
    mamba create --copy -p /env --file environment.lock
```

- 3. Clean and rebuild the Docker image (see [Usage](#usage))
If you get a **connection error**, open `localhost:8080` and log in as admin (also make sure you have the ClassX realm too).


- 4. After running a **full app test (MAKE SURE IT DOESN'T BREAK THE APP)**, run this command to ***edit the stable_env lock file***:

**USE `bash` OR `powershell` in the terminal (not cmd)**
```bash
cp ./environment/dev_env.lock ./environment/stable_env.lock
```

### Debugging:

#### 1. No Compatability
If there's no **linux-64** and/or **conda-forge** compatability with the dependency you want to add, *search for alternative names* (*ex:* `opencv` *has a conda-forge specific package called* `opencv-python`). 

#### 2. System Dependency (`lib`) Errors
If you get a `lib` error, find the `apt-get` library name and add it to the list of system dependecies (**located in the first build image**).

To find the **name** of the system dependency:

- 1. Comment out the **entire runtime image** and put the 2nd build-time image to `sleep` (you might need to comment the `target` keyword in the Dockerfile). Uncomment this `sleep` command in the **Dockerfile**:

```bash
ENTRYPOINT ["/bin/bash", "-c", "sleep infinity"]
```

- 2. Use this **command** to search for the `lib` you need to add:

```bash
apt-get search <keyword>
```

- 3. Add the new `lib` to this line in the **Dockerfile**:

```bash
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    [list of libs (add here)] \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

## Usage

To use this script, run it from the command line with the appropriate command and options.

```bash
python3 envmgr.py [command] [options]
```

### Available Commands

- `launch [options]`: Start the Docker environment.
- `status`: Display the status of containers and current volumes.
- `stop`: Shut down the Docker environment.
- `wipe`: Clean up all Docker objects, this will wipe everything!
- `clean`: Clean Docker environment, removing unused resources without affecting running containers.
- `shell [container_name]`: Open a shell into a specific container.
- `logs [container_name]`: View logs from a specific container.
- `restart [options]`: Restart the Docker environment.

### Command Options

- `launch`:
  - `detached`: Start the environment in detached mode (default).
  - `attached`: Start the environment with live logs (attached mode).
  - `fresh`: Stop containers, clean up old Docker images, and rebuild the environment.

- `restart`:
  - `detached`: Restart the environment in detached mode (default).
  - `attached`: Restart the environment with live logs (attached mode).

## Environment Variables

The script requires a `.env` file in the root directory to load specific environment variables. Ensure the following are added to your `.env` file.

### Sample `.env` File

```dotenv
# DOCKER (Add as needed)
CONTAINERS = 'dbx, appx, kcx, worker, redis'
```

## Error Handling

The script includes basic error handling using `try-except` blocks. If a subprocess command fails, it will print an error message in red.

### Example


```
[-] Failed to gather environment status.
```

## Scenarios

### 1. **Starting the Environment**

**Scenario:** You want to start your Docker environment in detached mode for normal operations.

**Command:**
```bash
python3 envmgr.py launch detached
```

**Explanation:**
- **Detached Mode:** Starts the Docker containers in the background. You can check logs and container status separately.
- **Expected Outcome:** The Docker environment starts without attaching to the terminal. You should see a confirmation message indicating successful start.

### 2. **Viewing Live Logs**

**Scenario:** You need to start the Docker environment and view live logs to monitor real-time activity.

**Command:**
```bash
python3 envmgr.py launch attached
```

**Explanation:**
- **Attached Mode:** Starts the Docker containers and attaches the terminal to the logs, allowing you to see real-time output.
- **Expected Outcome:** The Docker environment starts, and you see live logs directly in the terminal.

### 3. **Fresh Rebuild of Environment**

**Scenario:** You want to rebuild the Docker environment from scratch, cleaning up old images and build cache to free up disk space.

**Command:**
```bash
python3 envmgr.py launch detached fresh
```

**Explanation:**
- **Fresh Option:** Stops the current containers, removes old images, cleans up build cache, and rebuilds the environment.
- **Expected Outcome:** Old Docker resources are cleaned up, containers are stopped, images are rebuilt, and the environment starts in detached mode.

### 4. **Checking Environment Status**

**Scenario:** You need to check the status of all running containers, images, volumes, and networks.

**Command:**
```bash
python3 envmgr.py status
```

**Explanation:**
- **Status Command:** Displays detailed information about Docker containers, images, volumes, and networks.
- **Expected Outcome:** Lists current containers, images, volumes, and networks, helping you monitor your Docker setup.

### 5. **Stopping the Environment**

**Scenario:** You need to shut down the Docker environment to perform maintenance or updates.

**Command:**
```bash
python3 envmgr.py stop
```

**Explanation:**
- **Stop Command:** Stops and removes the Docker containers defined in the `dev.yml` file.
- **Expected Outcome:** The Docker containers are stopped, and you receive a confirmation message.

### 6. **Cleaning Up All Docker Objects**

**Scenario:** You want to clean up all Docker objects, including unused volumes and networks, to free up space and keep your Docker environment tidy.

**Command:**
```bash
python3 envmgr.py clean
```

**Explanation:**
- **Clean Command:** Re-launches environment to ensure only dangling objects get removed, removes dangling objects, stops environment.
- **Expected Outcome:** All unused containers, images, volumes, networks, and build cache are removed, and you receive a confirmation message.

### 7. **Accessing a Specific Container**

**Scenario:** You need to open a shell session into a specific container for debugging or manual operations.

**Command:**
```bash
python3 envmgr.py shell dbx
```

**Explanation:**
- **Shell Command:** Opens an interactive shell session inside the specified container (e.g., `dbx`).
- **Expected Outcome:** You gain access to a shell inside the `dbx` container, allowing you to execute commands and perform tasks inside the container.

### 8. **Restarting the Environment**

**Scenario:** You need to restart the Docker environment, applying changes and ensuring a clean start.

**Command:**
```bash
python3 envmgr.py restart detached
```

**Explanation:**
- **Restart Command:** Stops the environment, cleans up old resources, and restarts it in the specified mode (e.g., detached).
- **Expected Outcome:** The environment is stopped, cleaned up, and restarted in detached mode.

---

Feel free to adapt these scenarios based on your specific environment and needs. This guide will help developers understand how to effectively use the script for managing their Docker environments.

**By: Gian Sung :) and Rumi Khamidov :P**
