import subprocess


def install(ver=None):
    """
    Installation function for installing grafana to a linux machine
    ---------------------------
    Params

    param: ver: version required to be install
    ----------------------------
    Usage
    >>from enfinite_grafana.install_grafana import install
    >>install()
    installs the latest version of grafana available
    >>install(9.2.4)
    installs version-9.2.4
    """
    if ver:
        grafana_install_commands = [
            (
                "sudo apt-get install -y adduser libfontconfig1 iptables",
                "adding adduser and libfontconfig1",
            ),
            (
                f"wget https://dl.grafana.com/oss/release/grafana_{ver}_amd64.deb",
                "downloading grafana package",
            ),
            (f"sudo dpkg -i grafana_{ver}_amd64.deb", "installing grafana"),
            (f"rm grafana_{ver}_amd64.deb", "removing package files"),
            (
                "sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000",
                "remapping port:3000 -> 80",
            ),
        ]
    else:
        grafana_install_commands = [
            (
                "sudo apt-get install -y adduser libfontconfig1 grafana iptables",
                "installing grafana and related packages",
            ),
            (
                "sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000",
                "remapping port:3000 -> 80",
            ),
        ]
    p_ = None
    try:
        for process in grafana_install_commands:
            print(process[1] + "\n")
            p_ = subprocess.run(
                process[0],
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(p_.stdout)
    except Exception as e:
        print(f"error while installing: {e}")
        if p_:
            print(p_.stderr)


if __name__ == "__main__":
    install()
