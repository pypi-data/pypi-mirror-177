# TerraScope SDK

## Description

The `terrascope-sdk` is a convenience library that wraps the `terrascope-api` library. This is intended for internal OI users
only.

[Offical README](https://docs.terrascope.orbitalinsight.com/docs)

## Development Workflow

![TerraScope SDK Workflows](https://gitlab.com/orbitalinsight/terrascope_sdk/-/blob/master/.resources/terrascope-workflow.png "TerraScope SDK Workflows")<br>*Each lane builds on
what was generated in the prior*

## Installation

[Readme: Installation](https://terrascope.readme.io/docs/installation-1)

## Usage

TerraScope SDK is designed to simplify access to all the [terrascope-api](https://gitlab.com/orbitalinsight/oi_papi) calls
that are available. 

Each API uses a client object which requires the following env variables to be set:

```shell
TERRASCOPE_HOST=terrascope-api1.orbitalinsight.com
TERRASCOPE_TOKEN=<TerraScope API Token>
TERRASCOPE_TIMEOUT=<Int timeout in seconds> defalts to 60 seconds
```

## Authors and acknowledgment

Orbital Insight

## License

[LICENSE](LICENSE)

