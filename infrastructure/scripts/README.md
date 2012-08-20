# Scripts for operating cross region research resources

This folder gathers various scripts used during cross region operations currently. 
The goal is to provide a starting point for anyone who wants to reproduce this piece of research.

The scripts can be implemented in any language, though currently the team focuses on either 
Python with boto or PowerShell with the AWS SDK for .NET for its AWS automation tasks. 

## Requirements

The scripts are based on [Python 2.7](http://python.org/) and have the following dependencies:

* A recent version of [boto](https://github.com/boto/boto) (tested agains 2.5.2), which provides the interface to Amazon Web Services

## Installation

1.  Mac OSX 10.06 (Snow Leopard)
    * Ensure ```/usr/bin/python --version``` gives Python 2.7 +
    * ```sudo pip install boto argparse```
    * Add the following to your ```~/.bash_profile```
        ```
        export AWS_ACCESS_KEY_ID="AKIAI....."
		export AWS_SECRET_ACCESS_KEY="oF8S8UQ....."
		```

## Usage

The scripts provide common command line argument parsing and help functionality.

AWS credentials are obviously required, which can provided via the command line as well, 
but are more easily served via environment variables or a configuration file for day to day usage, 
see section [Getting Started with Boto](https://github.com/boto/boto#getting-started-with-boto) for details.

* The `validate-credentials` script provides a convenience method to both validate the AWS credentails and 
display respective account/user information, which helps when juggling multiple AWS accounts.

