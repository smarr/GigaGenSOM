# GigaGenSOM

GigaGenSOM generates sources files in the SOM (Simple Object Machine) language.
Its main goal is to generate large codebases that can be used to evaluate how
virtual machines cope with millions of lines of code.

## Goals

1. Generate code that can be parsed without error
2. Generate code that is executable
3. Generate code that shows somewhat realistic behavior
4. Have a tool that is independent of any specific SOM implementation
5. Keep it simple. This isn't a research project into how to generate code.

## Non-Goals

To scope the project the current set of non-goals includes:

1. Building a code generator as input for fuzzing
2. Building a pretty printer or automatic code formatter
3. Integrate with an existing SOM code base

## To Do

4. Generate Smalltalk-style methods
   - should size distribution be based on real data?


## Why Python

- this is considered tooling, most tooling in the SOM repos is either based on
  shell scripts or Python
- we need Python already for benchmarking
- we have PySOM/RPySOM as sources for some possibly relevant code bits
