# Parcel

## About

Running an mail server can be daunting, here are a bunch of different things to keep track of. You need to choose what software to use. Figure out how to configure it (properly) and how to maintain it.

If you are a seasoned sysadmin that prefer to tweak your systems to your likings this may not be for you. If you like a quick and easy way to run a fully functional e-mail server this is exactly what you are looking for!

### Configuration and software selection

E-mail is old and there are thousands of different ways to manage a mail server. To keep the scope somewhat limited the software selection is restricted to what this project considers "the best" software for this task. The same idea is applied to the configuration.

## Technology

Parcel is actually a configuration and provision tool that provisions the actual mail servers inside LXD containers. You can change all configuration via a friendly web-based UI. If you prefer the CLI all options can be changed from the shell.

## Requirements

* A Linux-server open to the internet (that can run snapd)
* The LXD snap installed locally
* A domain (like example.com or mail.example.com)

## Install

Install the snap on a public server, preferably not on a home server due the fact that most home connections are blacklisted due to spam.

```
$ snap install parcel
```

The above command will install the stable release. If you like to install the candidate channel run `snap install --candidate parcel`.

| Channel | Description |
| ------- | ----------- |
| stable  | A tested stable release, recommended for most users |
| candidate | The upcoming stable release, I think this one is stable but it's here to test it before I promote it to stable |
| beta | Beta releases for more experimental upcoming releases, please report bugs. |
| edge | The latest code in master of this repository, this is **absolutely not** stable |

Now run `parcel` in a terminal and follow the instructions.

## History

A few years back I moved away from Gmail to my self hosted solution and
I have been happy with the result. This snap is the second iteration of
that install. This install will probably be different compared to the
original one, but it is still based around my needs and what I think
a mail server should contain.
