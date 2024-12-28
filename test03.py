import asyncio
import subprocess
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Constants
CONTAINER_ID = "3f6576dca0b9"
LLM_PROMPT = '--image /images/download.jpeg "Describe the image and answer in English."'
TIMEOUT = 300  # seconds (adjust as needed)

async def run_command(cmd, input_data=None, timeout=TIMEOUT):
    """
    Runs a shell command asynchronously, optionally sends input_data to its stdin,
    and returns the output.
    """
    try:
        logging.info(f"Running command: {' '.join(cmd)}")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE if input_data else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=input_data.encode() if input_data else None),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            logging.error(f"Command '{' '.join(cmd)}' timed out after {timeout} seconds.")
            raise

        if process.returncode != 0:
            error_message = stderr.decode().strip() if stderr else "Unknown error"
            logging.error(f"Command failed: {' '.join(cmd)}")
            logging.error(f"Error: {error_message}")
            raise subprocess.CalledProcessError(
                process.returncode, cmd, output=stdout, stderr=stderr
            )

        output = stdout.decode().strip()
        if output:
            logging.info(f"Command output: {output}")
        return output

    except Exception as e:
        logging.error(f"Error running command {' '.join(cmd)}: {e}")
        raise

async def start_container(container_id):
    """
    Starts the specified Docker container.
    """
    logging.info(f"Starting container {container_id}...")
    cmd = ["docker", "start", container_id]
    await run_command(cmd)
    logging.info(f"Container {container_id} started successfully.")

async def stop_container(container_id):
    """
    Stops the specified Docker container.
    """
    logging.info(f"Stopping container {container_id}...")
    cmd = ["docker", "stop", container_id]
    await run_command(cmd)
    logging.info(f"Container {container_id} stopped successfully.")

async def exec_llm_command(container_id, prompt):
    """
    Executes the LLM command inside the Docker container and sends the prompt via stdin.
    """
    logging.info(f"Executing LLM command inside container {container_id}...")
    cmd = ["docker", "exec", "-i", container_id, "ollama", "run", "llava-llama3"]

    # Run the command and send the prompt via stdin
    output = await run_command(cmd, input_data=prompt, timeout=TIMEOUT)
    logging.info("LLM Output:")
    logging.info(output)
    return output

async def main():
    try:
        # Start the Docker container
        await start_container(CONTAINER_ID)

        # Define the prompt to send to the LLM
        prompt = LLM_PROMPT

        # Execute the LLM command and send the prompt
        llm_output = await exec_llm_command(CONTAINER_ID, prompt)

        # Process the LLM output as needed
        # For demonstration, we'll just log it
        logging.info("\nFinal Output:")
        logging.info(llm_output)

    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(e.cmd)}' failed with return code {e.returncode}")
        if e.output:
            logging.error(f"Output: {e.output.decode().strip()}")
        if e.stderr:
            logging.error(f"Error: {e.stderr.decode().strip()}")
    except asyncio.TimeoutError:
        logging.error("The LLM command did not complete in time.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the container is stopped regardless of success or failure
        try:
            await stop_container(CONTAINER_ID)
        except Exception as e:
            logging.error(f"Error stopping container {CONTAINER_ID}: {e}")

# Entry point
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
        sys.exit(0)