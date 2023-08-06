import datetime
import logging
import os
import sys
from datetime import datetime
from subprocess import run, check_output
import pathlib
from rpamaker.orquestador import OrquestadorAPI


def get_base_path():
    # file_path = sys.argv[0]
    # file_location = os.path.dirname(file_path)
    file_location = os.getcwd()
    return file_location


def call_robot(keyword, variables, t_id):
    library_path = pathlib.Path(__file__).parent.resolve()
    root_path = get_base_path()
    base_path = os.path.join(root_path, f'{keyword}/')

    logging.info(f'call_robot: {keyword} {variables} {base_path}')

    output_path = os.path.join(base_path, 'output/')
    robot_path = os.path.join(base_path, f'tasks.robot')

    d = datetime.strftime(datetime.now(), '%y%m%d%H%M%S%f')
    output_file = 'output-' + d + '.xml'
    log_file = 'log-' + d + '.html'
    report_file = 'report-' + d + '.html'

    command = [
        os.path.join(base_path, 'venv/Scripts/python.exe'),
        '-m',
        'robot',
        '--pythonpath', base_path,
        '--listener', 'rpamaker.listener.Listener',
        *variables,
        '--log', os.path.join(output_path, log_file),
        '--output', os.path.join(output_path, output_file),
        '--report', os.path.join(output_path, report_file),
        robot_path,
    ]

    result = run(
        command,
        shell=True,
        capture_output=True,
    )

    if result.stderr:
        orquestador = OrquestadorAPI(t_id)
        orquestador.send_status('FAILURE', 'Error al ejecutar el robot')
        orquestador.send_logs_infra(f"{result.stderr.decode('utf-8')}")

# def call_robot(keyword, variables):
#     base_path = get_base_path()
#     logging.info(f'call_robot: {keyword} {variables} {base_path}')
#
#     output_path = os.path.join(base_path, 'output/')
#     robot_path = os.path.join(base_path, f'{keyword}.robot')
#
#     d = datetime.strftime(datetime.now(), '%y%m%d%H%M%S%f')
#     output_file = 'output-' + d + '.xml'
#     log_file = 'log-' + d + '.html'
#     report_file = 'report-' + d + '.html'
#     robot.run(
#         robot_path,
#         # loglevel='DEBUG',
#         listener=Listener(),
#         variable=variables,
#         log=output_path + log_file,
#         output=output_path + output_file,
#         report=output_path + report_file
#     )
