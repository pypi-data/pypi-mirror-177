import subprocess


def uninstall():
    """
    Uninstalls the grafana from the linux machine
    """
    grafana_install_commands = [
        ("sudo apt-get remove -y libfontconfig1", "removing  libfontconfig1 grafana"),
        # ('sudo apt autoremove -y', 'autoremove left packages'),
        # ('wget https://dl.grafana.com/oss/release/grafana_9.2.0_amd64.deb', 'downloading grafana package'),
        # ('sudo apt-get remove -i grafana_9.2.0_amd64.deb', 'uninstalling grafana'),
        # ('rm grafana_9.2.0_amd64.deb','removing package files'),
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
    uninstall()
