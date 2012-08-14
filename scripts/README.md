# Scripts for operating cross region research resources

This folder gathers various scripts used during cross region operations currently. 
The goal is to provide a starting point for anyone who wants to reproduce this piece of research.

The scripts can be implemented in any language, though currently the team focuses on either 
Python with boto or PowerShell with the AWS SDK for .NET for its AWS automation tasks. 

## Requirements

The scripts are based on [Python 2.7](http://python.org/) and have the following dependencies:

* [boto](https://github.com/boto/boto), which provides the interface to Amazon Web Services

## Usage

The scripts provide common command line argument parsing and help functionality.

AWS credentials are obviously required, which can provided via the command line as well, 
but are more easily served via environment variables or a configuration file for day to day usage, 
see section [Getting Started with Boto](https://github.com/boto/boto#getting-started-with-boto) for details.

