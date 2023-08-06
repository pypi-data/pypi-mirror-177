import argparse
import sys
import yaml
import os
import glob
import json
from schema import Schema, SchemaError, Or
from textwrap import wrap
from termcolor import colored
from docker_runner import execute_steps
from git import Repo
from tempfile import TemporaryDirectory

STATUS_CHARACTERS = {
    "pass": ' ✓',
    "warning": ' !',
    "security": ' ✘!',
    "fail": ' ✘',
    "info": ' i'
}

RULE_SCHEMA = Schema({
    "name": str,
    "image": str,
    "tags": [str],
    "steps": [str],
    "type": Or("warning", "security", "fail", "info")
}, ignore_extra_keys=True)

def intersection(lst1, lst2):
    lst2 = [name.upper() for name in lst2]
    return [value for value in lst1 if value.upper() in lst2]

def verify_single_rule(args, rule):
    if len(intersection(rule['tags'], args.tags)) > 0:
        _print(args, rule['name'].ljust(50, '.'), end='')
        
        env = {
            'COMPLIANCE_RULE_NAME': rule['name'],
            'COMPLIANCE_RULE_TYPE': rule['type'],
            'COMPLIANCE_TAGS': ",".join(args.tags)
        }

        for e in args.env:
            e = e.split('=')
            env[e[0]] = e[1]

        output_result = execute_steps(rule['image'], args.target, rule['steps'], env)
        
        _verbose(args, '\n')
        _print_result(args, output_result)

        if output_result[0]:
            _print(args, STATUS_CHARACTERS["pass"])
            _json_result(args, rule['name'], output_result, "pass")
            return "pass"
        else:
            _print(args, STATUS_CHARACTERS[rule['type']])
            _print_fail_only(args, output_result)
            _json_result(args, rule['name'], output_result, rule['type'])
            return rule['type']

    else:
        _verbose(args, "No matching tags, skipping rule file")
        return None

json_output = {
    "checks": []
}
def _json_print(args, results):
    if args.output == 'json':
        json_output['target'] = args.target
        json_output['results'] = results
        print(json.dumps(json_output, indent=4))

def _json_result(args, rule_name, output, status):
    if args.output == 'json':
        json_output["checks"].append({
            "status": status,
            "ruleName": rule_name,
            "steps": [{
                "exitCode": i[0],
                "step": i[1],
                "output": i[2].decode("utf-8")
            } for i in output[1]]
        })

def _print_docker_output(args, result):
    for line_exec in result[1]:
        exit_message = None
        if line_exec[0] == 0:
            exit_message =  " (Exit Code: "+ colored("0", 'green') + ")"
        else:
            exit_message = " (Exit Code: "+ colored(line_exec[0], 'red') + ")"

        _print(args, "\t" + colored(line_exec[1], attrs=['underline']) + exit_message)
        for line in line_exec[2].splitlines():
            _print(args, '\t\t'+ line.decode("utf-8"))

def _print_result(args, result):
    if args.verbose:
        _print_docker_output(args, result)

def _print_fail_only(args, result):
    if (not args.verbose) and (not args.hide_fail):
        _print_docker_output(args, result)

def _verbose(args, message):
    if args.verbose:
        print(message)

def _print(args, message, end="\n"):
    if args.output == None:
        print(message, end=end)

def is_git_target(target):
    return target.startswith('http') or target.startswith('git') or target.startswith('ssh')

def run_compliance(args):
    args.tags.append('all')

    _print(args, "Checking compliance for " + args.target)

    results = {
        'warning': 0,
        'security': 0,
        'fail': 0,
        'pass': 0,
        'info': 0,
        'total_tests': 0
    }

    with TemporaryDirectory() as temp_dir:
        if is_git_target(args.target):
            _print(args, "Target is a git URL- cloning repository")
            _verbose(args, "Checking out git repo to " + temp_dir)
            _print(args, "Cloning git repo".ljust(50, '.'), end='')
            Repo.clone_from(args.target, 
                temp_dir, 
                multi_options=["--depth=1"], 
                branch=args.branch)
            _print(args, STATUS_CHARACTERS["pass"])
            args.target = temp_dir

        rule_files = glob.glob(args.rules, recursive=True)
        for filename in rule_files:
            _verbose(args, "Using rule file "+ filename)
            with open(filename, 'r') as stream:
                rule = yaml.safe_load(stream)
                try:
                    RULE_SCHEMA.validate(rule)
                except SchemaError as se:
                    print("Rule file {file} is invalid!".format(file=filename))
                    raise se
                response = verify_single_rule(args, rule)
                if response:
                    results[response] += 1
                    results['total_tests'] += 1
        
    _print(args, "{total_tests} tests ({pass} pass, {info} info, {warning} warning, {fail} fail, {security} security)".format(**results))
    _json_print(args, results)

    if args.no_error:
        sys.exit(0)

    if results['security'] > 0 or results['fail'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

def list_rules(args):
    rule_files = glob.glob(args.rules, recursive=True)
    for filename in rule_files:
        with open(filename, 'r') as stream:
            rule = yaml.safe_load(stream)
            try:
                RULE_SCHEMA.validate(rule)
            except SchemaError as se:
                print("Rule file {file} is invalid!".format(file=filename))
                raise se
            print("{name} ({type}) ".format(
                name=rule['name'], 
                type=rule['type']
            ).ljust(80, '-'))
            print("""File:\t{filename}
Tags:\t{tags}
Description:
{description}
""".format(
                filename=filename,
                description="\n".join(wrap(rule['description'], subsequent_indent='\t', initial_indent='\t')),
                tags=",".join(rule['tags'])))


def main():
    parser = argparse.ArgumentParser(description="Run compliance checks against a project")
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers()

    parser_run = subparsers.add_parser('run')
    parser_run.add_argument("-r", "--rules", help="glob of rule files", default="rules/**/*.yml")
    parser_run.add_argument("-v", "--verbose", help="increase output verbosity", action='store_true')
    parser_run.add_argument("-f", "--hide-fail", help="hide failure out information", action='store_true')
    parser_run.add_argument("--no-error", help="dont exit 1 if security and fails are found", action='store_true')
    parser_run.add_argument("-t", "--tags", help="project tags", action='append', default=[])
    parser_run.add_argument("-e", "--env", help="environmental variables", action='append', default=[])
    parser_run.add_argument("--output", help="output type", choices=["json"])
    parser_run.add_argument("-b", "--branch", help="the branch to use if target is a git repo", default="master")
    parser_run.add_argument("target", help="the target folder or git repo to run the compliance check on")
    parser_run.set_defaults(func=run_compliance)

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument("-r", "--rules", help="glob of rule files", default="rules/**/*.yml")
    parser_list.set_defaults(func=list_rules)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

