#! /usr/bin/env python3

from agent.workflows.graph import graph


def main():
    graph.invoke({"target_file_path": "test.py"})


if __name__ == "__main__":
    main()
