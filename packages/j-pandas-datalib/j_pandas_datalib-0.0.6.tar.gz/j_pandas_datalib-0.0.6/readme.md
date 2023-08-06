# Python Datalib

Useful Python abstractions around the Pandas file Interaction and other common Tasks.

## VS Code Devcontainer

This workspace contains a [Vscode devcontainer](https://code.visualstudio.com/docs/remote/containers).

## Development

### Bump / Release Version

- Trigger [Version Bump](https://github.com/OpenJKSoftware/j-pandas-datalib/actions/workflows/version-bump.yml) pipeline with appropriate target.
- Merge the created PullRequest
- This will create a Tag on `main`
- Create a realease from this Tag. The Pipeline will automatically push to [Pypi](https://pypi.org/project/j-pandas-datalib/)
