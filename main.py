from fastmcp import FastMCP
import paramiko
import os

mcp = FastMCP("RemoteSSHGateway")


@mcp.tool()
def run_remote_command(command: str) -> str:
    """Executes a command securely on the target remote Linux server over SSH."""

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            hostname=os.environ.get("MY_SERVER_DOMAIN"), 
            port=os.environ.get("MY_SERVER_PORT"),
            username=os.environ.get("MY_SERVER_USERNAME"),  # Replace with your Linux username
            password=os.environ.get("MY_SERVER_PASSWORD"),
            timeout=15
        )
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        ssh.close()
        
        return output if output else error
    except Exception as e:
        return f"SSH Connection Failed: {str(e)}"

if __name__ == "__main__":
    # Cloud Run populates the PORT env variable automatically
    port = int(os.environ.get("PORT", 8000))
    print("Getting ready to start SSH with port %d!" % port)
    mcp.run(transport="http", port=port)

