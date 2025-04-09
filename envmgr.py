import subprocess
import sys
import os
from dotenv import load_dotenv

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Logo
ART = ''' \033[92m
   ____              __  ___                                        ___
  / __/___  _  __   /  |/  /___ _ ___  ___ _ ___ _ ___  ____  _  __<  /
 / _/ / _ \| |/ /  / /|_/ // _ `// _ \/ _ `// _ `// -_)/ __/ | |/ // /
/___//_//_/|___/  /_/  /_/ \_,_//_//_/\_,_/ \_, / \__//_/    |___//_/
                                           /___/
                                                        By: Gian Sung
'''
def help():
    print(f"""{GREEN}
    Usage: python3 envmgr.py [command] [options]{RESET}

    Available commands:
    - launch [options]: Start the environment in detached mode (default) or live mode

    - status: Displays container status, current images, volumes, and networks.

    - stop: Shut down the Docker environment.

    - wipe: Clean all Docker objects, including images, volumes, and cache.

    - clean: Clean Docker environment, removing unused resources without affecting running containers.

    - shell [container_name]: Shell into a specific container. Special handling for 'dbx' container to use MySQL client.

    - logs [container_name]: View logs from a specific container.

    - restart [options]: Restart the environment.
     """)   

# def help():
#     print("""
#     Usage: python3 envmgr.py [command] [options]
#
#     Available commands:
#     - launch [options]: Start the environment in detached mode (default) or live mode
#     - status: Displays container status and current volumes.
#     - stop: Shut down docker environment
#     - wipe: Clean all Docker objects including unused volumes
#     - shell [container_name]: Shell into a specific container
#     - restart [options]: Restart the environment in detached option (default) or live option
#     - logs [container_name]: View logs from a specific container
#     """)

def load_env_vars():
    """Load environment variables from .env file."""
    load_dotenv()
    containers = [container.strip() for container in os.getenv("CONTAINERS", "").split(',')]
    return {
        "dbx_password": os.getenv("MYSQL_ROOT_PASSWORD"),
        "containers": containers
    }

def cleanup_old_resources():
    """Clean up old Docker images, build cache, and unused volumes."""
    try:
        print(f"{GREEN}[*] Removing unused Docker images...{RESET}")
        subprocess.run(["docker", "image", "prune", "-a", "-f"], check=True)
        print(f"{GREEN}[+] Removed unused Docker images{RESET}")
        print()

        print(f"{GREEN}[*] Cleaning up Docker build cache...{RESET}")
        subprocess.run(["docker", "builder", "prune", "-a", "-f"], check=True)
        print(f"{GREEN}[+] Cleaned up Docker build cache.{RESET}")
        print()

        print(f"{GREEN}[*] Removing unused Docker volumes...{RESET}")
        subprocess.run(["docker", "volume", "prune", "-a", "-f"], check=True)
        print(f"{GREEN}[*] Removed unused Docker volumes.{RESET}")
        print()

        print(f"{GREEN}[*] Removing unused networks...{RESET}")
        subprocess.run(["docker", "network", "prune", "-f"], check=True)
        print(f"{GREEN}[+] Removed unused networks.{RESET}")
        print()

        print(f"{GREEN}[*] Removing stopped containers...{RESET}")
        subprocess.run(["docker", "container", "prune", "-f"], check=True)
        print(f"{GREEN}[+] Removed stopped containers.{RESET}")
        print()
    except subprocess.CalledProcessError:
        print(f"{RED}[-] Failed to clean up Docker resources.{RESET}")

def launch(mode="detached", fresh=False):
    try:
        # Clean up old resources if fresh is True
        if fresh:
            print(f"{GREEN}[*] Cleaning up old Docker resources...{RESET}")
            cleanup_old_resources()

            print(f"{GREEN}[*] Stopping containers and rebuilding images...{RESET}")
            subprocess.run(["docker", "compose", "-f", "dev.yml", "down"], check=True)
            subprocess.run(["docker", "compose", "-f", "dev.yml", "build"], check=True)
        
        # Start the environment in the selected mode
        if mode == "detached":
            subprocess.run(["docker", "compose", "-f", "dev.yml", "up", "-d"], check=True)
            print(f"{GREEN}[+] Application started in detached mode!{RESET}")
        elif mode == "attached":
            print(f"{GREEN}[+] Application started with live logs!{RESET}")
            subprocess.run(["docker", "compose", "-f", "dev.yml", "up"], check=True)
        else:
            print(f"{RED}[-] Invalid mode! Use 'detached' or 'attached'.{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}[-] Failed to start the application in {mode} mode.{RESET}")

def status():
    try:
        # Prints all container status 
        subprocess.run(["docker", "ps", "-a"])
        print()
        print(f"{GREEN}[*] Displaying current images:{RESET}")
        subprocess.run(["docker", "image", "ls"])
        print()
        print(f"{GREEN}[*] Displaying current volumes:{RESET}")
        subprocess.run(["docker", "volume", "ls"])
        print()
        print(f"{GREEN}[*] Displaying current networks:{RESET}")
        subprocess.run(["docker", "network", "ls"])
        print()
    except subprocess.CalledProcessError:
        print(f"{RED}[-] Failed to gather environment status.{RESET}")

def stop():
    try:
        # Stop docker containers from dev.yml file"
        subprocess.run(["docker", "compose", "-f", "dev.yml", "down"])
        print(f"{GREEN}[+] Environment shutdown successful!{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}[-] Failed to shut down the environment.{RESET}")

def clean():
    try:
        # Re-launches environment in detached mode, to ensure only dangling objects get Removed
        launch(mode="detached", fresh=False)
        cleanup_old_resources()
        stop()
        print(f"{GREEN}[+] Environment cleaned successfully!{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}[-] Failed to clean Docker environment.{RESET}")


def wipe():
    try:
        # Stops and deletes containers, prunes images, volumes, cache, and system
        stop()
        cleanup_old_resources()
        print(f"{GREEN}[+] Docker system wiped clean!{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}[-] Failed to wipe Docker system.{RESET}")

def shell(container_name):
    env_vars = load_env_vars()
    containers = env_vars["containers"]
    try:
        if container_name not in containers:
            print(f"{RED}[-] Invalid container name! Valid names are: {', '.join(containers)}.{RESET}")
            return

        print(f"{GREEN}[+] Attempting to shell into container {container_name}:{RESET}")

        if container_name == 'dbx' and env_vars["dbx_password"]:
            # Use MySQL client for dbx container
            subprocess.run([
                "docker", "exec", "-it", container_name,
                "mysql", "-u", "root", "-p" + env_vars["dbx_password"]
            ], check=True)
        else:
            subprocess.run(["docker", "exec", "-it", container_name, "/bin/bash"], check=True)
    except subprocess.CalledProcessError:
        print(f"{RED}[-] Failed to shell into {container_name} container.{RESET}")
        print(f"{RED}[-] Ensure container {container_name} is running.{RESET}")

def logs(container_name):
    env_vars = load_env_vars()
    containers = env_vars["containers"]
    try:
        if container_name not in containers:
            print(f"{RED}[-] Invalid container name! Valid names are: {', '.join(containers)}.{RESET}")
            return

        print(f"{GREEN}[+] Fetching logs for container {container_name}:{RESET}")
        subprocess.run(["docker", "logs", container_name], check=True)
    except subprocess.CalledProcessError:
        print(f"{RED}[-] Failed to retrieve logs from container {container_name}.{RESET}")
        print(f"{RED}[-] Ensure container {container_name} is running.{RESET}")

if __name__ == "__main__":
    print(ART)

    # Default values
    mode = None
    fresh = False

    # Parse command line arguments
    if len(sys.argv) < 2:
        help()
    else:
        command = sys.argv[1].lower()

        if command == "launch":
            mode = "detached" if len(sys.argv) < 3 else sys.argv[2].lower()
            fresh = "fresh" in sys.argv
            launch(mode, fresh)
        elif command == "wipe":
            wipe()
        elif command == "shell":
            if len(sys.argv) == 3:
                shell(sys.argv[2].lower())
            else:
                print(f"{RED}[-] Missing container name for 'shell' command.{RESET}")
                help()
        elif command == "logs":
            if len(sys.argv) == 3:
                logs(sys.argv[2].lower())
            else:
                print(f"{RED}[-] Missing container name for 'logs' command.{RESET}")
                help()
        elif command == "restart":
            #fresh = " in sys.argv
            stop()
            print(f"{GREEN}[+] Restarting environment {RESET}")
            mode = "detached" if len(sys.argv) < 3 else sys.argv[2].lower()
            #cleanup_old_resources()
            launch(mode, fresh=False)
            #cleanup_old_resources()
        elif command == "stop":
            print(f"{GREEN}[+] Shutting down environment {RESET}")
            stop()
        elif command == "status":
            print(f"{GREEN}[*] Displaying container status:{RESET}")
            status()
        elif command == "clean":
            print(f"{GREEN}[*] Cleaning Docker environment:{RESET}")
            clean()

        else:
            help()

