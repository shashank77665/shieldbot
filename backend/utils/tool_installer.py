import subprocess

def install_security_tools(tools):
    """
    Simulate installation of security testing tools on a Linux system.
    In production, you could use subprocess to run installation commands,
    e.g., using "sudo apt-get install -y <tool>".
    For demonstration, this function returns simulated responses.
    """
    installed = {}
    for tool in tools:
        try:
            # Uncomment the following line to run an actual installation,
            # but use with caution!
            # subprocess.check_call(["sudo", "apt-get", "install", "-y", tool])
            installed[tool] = "Simulated installation success"
        except subprocess.CalledProcessError as e:
            installed[tool] = f"Installation failed: {str(e)}"
    return installed