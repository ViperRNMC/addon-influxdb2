#!/usr/bin/env python3
import urllib.request
import re

GITHUB_RELEASES_URL = "https://github.com/influxdata/influxdb/releases"

def get_latest_influxdb2():
    with urllib.request.urlopen(GITHUB_RELEASES_URL) as response:
        html = response.read().decode("utf-8")

    # Print alle href-links van de GitHub releases pagina
    href_links = re.findall(r'href="([^"]+)"', html)
    # print("Alle href-links op de pagina:")
    # for link in href_links:
    #     print(link)

    # Filter tar.gz bestanden met "influxdb2" of "influxdb2-client" in de link en eindigend op .tar.gz
    tar_files = [link for link in href_links if (("influxdb2" in link or "influxdb2-client" in link) and link.endswith(".tar.gz"))]

    server_releases = {}
    client_releases = {}
    for f in tar_files:
        filename = f.split("/")[-1]
        # Haal versie en architectuur uit bestandsnaam, voorbeeld: influxdb2-2.6.1_linux_amd64.tar.gz of influxdb2-client-2.6.1_linux_amd64.tar.gz
        match_server = re.match(r'influxdb2-(\d+\.\d+\.\d+)_linux_(.+)\.tar\.gz', filename)
        match_client = re.match(r'influxdb2-client-(\d+\.\d+\.\d+)_linux_(.+)\.tar\.gz', filename)
        if match_server:
            version, arch = match_server.groups()
            if version not in server_releases:
                server_releases[version] = []
            if arch not in server_releases[version]:
                server_releases[version].append(arch)
        elif match_client:
            version, arch = match_client.groups()
            if version not in client_releases:
                client_releases[version] = []
            if arch not in client_releases[version]:
                client_releases[version].append(arch)

    if not server_releases:
        print("Geen InfluxDB 2.x server releases gevonden.")
    else:
        latest_server_version = sorted(server_releases.keys(), key=lambda s: list(map(int, s.split('.'))))[-1]
        print(f"Laatste InfluxDB 2.x server versie: {latest_server_version}")
        print("Beschikbare architecturen server:", ", ".join(sorted(server_releases[latest_server_version])))

    if not client_releases:
        print("Geen InfluxDB 2.x client releases gevonden.")
    else:
        latest_client_version = sorted(client_releases.keys(), key=lambda s: list(map(int, s.split('.'))))[-1]
        print(f"Laatste InfluxDB 2.x client versie: {latest_client_version}")
        print("Beschikbare architecturen client:", ", ".join(sorted(client_releases[latest_client_version])))

if __name__ == "__main__":
    get_latest_influxdb2()
