# Gabi MCP server

This repo contains a MCP server for [gabi](https://github.com/app-sre/gabi).

For now, to run it within vscode with copilot for example:

* clone this repository
* run `make build` (uses podman)
* `oc login` to the cluster running gabi
* add the following the your vscode workspace `.vscode/mcp.json` file:

```json
{
  "servers": {
    "gabi": {
      "type": "stdio",
      "command": "podman",
      "args": [
        "run",
        "-i",
        "-e",
        "GABI_ENDPOINT=<your Gabi instance URL>",
        "-e",
        "GABI_TOKEN=<Your Openshift token: oc whoami -t>",
        "localhost/gabi-mcp-server:latest"
      ]
    }
  }
}
```

You can now chat with Copilot in VSCode:

```
run `select * from cars` on gabi and show the output
```

Example output (from real life):

> I'll run a SQL query on Gabi to show you all data from the cars table. First, I need to check if the Gabi server is available and ready.
> 
> Ran `check` on gabi (MCP Server)
>
> Great! The Gabi server is reachable and ready. Now I'll run your SQL query to select all data from the cars table.
> 
> Ran `query` on gabi (MCP Server)
>
> Here are the results of your query `SELECT * FROM cars`:
> 
> | brand	| model	  | year |
> |---------|---------|------|
> | Ford	| Mustang | 1964 |
>
> As you can see, there's one row in the cars table with a Ford Mustang
