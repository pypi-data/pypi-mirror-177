# Python Datalib

Useful Python abstractions around the Pandas file Interaction and other common Tasks.

## VS Code Devcontainer

This workspace contains a [Vscode devcontainer](https://code.visualstudio.com/docs/remote/containers).

## Development

### Bump version

- Run `poetry version <minor|major|patch|...>` [Valid Values for Version target](https://python-poetry.org/docs/cli/#version).
- Push commit with `[BUMP] Prefix`

### Release

- Create new Release in Github
- Action will automatically create a Tag and push to pypi
