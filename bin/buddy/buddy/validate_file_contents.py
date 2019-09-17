import argparse

from buddy.validation_workflow import ValidationWorkflow


def setup_workflow(yaml_file):
    workflow = ValidationWorkflow.from_yaml_file(yaml_file)
    return workflow


def run_workflow(yaml_file):
    workflow = setup_workflow(yaml_file)
    report = workflow.format_failure_report()
    if report:
        print(report)


def define_command_arg_parser():
    """
    Get a parser that extracts the command args used when calling this program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("validate_yaml", nargs=1)
    return parser


# ---- run as a script

if __name__ == "__main__":
    ARGS = define_command_arg_parser().parse_args()
    run_workflow(ARGS.validate_yaml[0])
