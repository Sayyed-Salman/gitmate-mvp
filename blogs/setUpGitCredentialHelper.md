# Setting up `git credential helper`

## Install GCM

- https://github.com/git-ecosystem/git-credential-manager

## Setup GCM

To save and fetch credentials from the Windows Credential Manager, you can use the following command:

```bash
git config --global credential.helper manager
```

To do the same on linux, you can use the following command:

```bash
git config --global credential.helper store --path=~/.gitmate
```
