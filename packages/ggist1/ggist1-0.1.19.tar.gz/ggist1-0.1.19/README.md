# Hi 

**ggist** is a terminal utility to find and create:
- aliases
- scripts


## Getting Started
The easiest way to install GGist's CLI is using the install script:

```
# Copy and run command to install the CLI.
bash -c "$(curl -fsSL https://raw.githubusercontent.com/mzsrtgzr2/ggist/main/install.sh)"
```


# Add new aliases and scripts
Currently only demo - 

```
ggist add source demo/k8s
ggist add source demo/git
ggist add source demo/docker
ggist add source demo/awscli
ggist add source demo/zsh
ggist add source demo/team1
ggist add source demo/osx
```

### Run scripts
for example, Team1 have an onboarding script.
run it, you will be prompt to approve every step:
```
ggist run team1.onboarding
```

to see all available scripts run `ggist show scripts`

** Make sure you open a new terminal to see the changes **

### to see all your sources
```
ggist show sources
```

### See all your aliases
```
ggist show aliases
```

### See all your scripts
```
ggist show aliases
```


## Vision 

manage your aliases and scripts
    - get new from community 
    - create your own
    - complicated installations in one command
    - synchronize in your team


## TODO:
- grafana runner - query
- jenkins runner - query