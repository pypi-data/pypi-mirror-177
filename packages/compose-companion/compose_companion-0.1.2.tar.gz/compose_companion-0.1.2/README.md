# Compose Companion

This is a little CLI tool created for my home server.

It aims to make it easy to configure and document scripts that should run before and/or after the server containers on docker compose go up or down.

## Scrips File

The app will read the scripts from a yaml file in the following format:

```yaml
# compose-companion.yaml

x-before-up:
  sonarr:
    - echo this will run before sonarr startup
    - echo this too will run before sonarr startup, after the previous one
  radarr:
    - echo this will run before radarr startup
    - echo this too will run before radarr startup, after the previous one

x-after-up:
  sonarr:
    - echo this will run after sonarr startup
    - echo this too will run after sonarr startup, after the previous one
  radarr:
    - echo this will run after radarr startup
    - echo this too will run after radarr startup, after the previous one

x-before-down:
  sonarr:
    - echo this will run before sonarr shutdown
    - echo this too will run before sonarr shutdown, after the previous one
  radarr:
    - echo this will run before radarr shutdown
    - echo this too will run before radarr shutdown, after the previous one

x-after-down:
  sonarr:
    - echo this will run after sonarr shutdown
    - echo this too will run after sonarr shutdown, after the previous one
  radarr:
    - echo this will run after radarr shutdown
    - echo this too will run after radarr shutdown, after the previous one
```

The container keys should match the ones from `docker-compose.yaml` file.  
The app will look for a file named `compose-companion.yaml` on the folder it's first run, if that's not there it'll ask you to inform the file path manually.  
As the top-level keys start with `x-`, you can use the `docker-compose.yaml` file itself, if you wish, and these settings will be properly ignored by docker compose.

## Commands

```plain
╭─ Commands ────────────────────────────────────────────────────────────────────╮
│ up         Starts up target containers. If no target is defined, starts all   │
│            containers. Equivalent to `docker compose up -d`                   │
│                                                                               │
│ pause      Pauses target containers. If no target is defined, pauses all      │
│            containers. Equivalent to `docker compose stop`                    │
│                                                                               │
│ down       Shuts down target containers. If no target is defined, shuts down  │
│            all containers. Equivalent to `docker compose rm -sf` or `docker   │
│            compose down`                                                      │
│                                                                               │
│ logs       Prints logs for target containers. If no target is defined, prints │
│            for all running ones. Equivalent to `docker compose logs -f`       │
│                                                                               │
│ config     View or change configurations.                                     │
╰───────────────────────────────────────────────────────────────────────────────╯
```

For more details on each command, run `compose [command] --help`
