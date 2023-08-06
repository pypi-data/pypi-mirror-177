from pathlib import Path
from typing import get_type_hints

from fire import Fire
from wheel_inspect import inspect_wheel

from ksqldb_udf import run_command
from ksqldb_udf.java import UdfHandler, UdfClass, UdfPackage, UdfParameter, KsqldbUdfTypes
from sys import executable

_udf_type_to_default_value = {
    int: -1,
    float: float('nan'),
    str: 'ERROR',
    bool: False
}

_python_type_to_ksqldb_type = {
    int: KsqldbUdfTypes.long,
    float: KsqldbUdfTypes.double,
    str: KsqldbUdfTypes.String,
    bool: KsqldbUdfTypes.boolean
}


def _install(wheel_path):
    stdout = run_command(executable, '-m', 'pip', 'install', str(wheel_path))
    print(stdout)


def build_jar_from_wheel(wheel_path: str, target_dir: str = '', group_id: str = ''):
    wheel_path = Path(wheel_path)
    assert wheel_path.exists(), f'{wheel_path} does not exist'
    target_dir = Path(target_dir) if target_dir else wheel_path.parent
    # _install(wheel_path)

    wheel_metadata = inspect_wheel(wheel_path)
    dist_info = wheel_metadata['dist_info']
    try:
        entry_points = dist_info['entry_points']['ksqldb']
    except KeyError as e:
        raise 'Wheel must define ksqldb entrypoints' from e

    package_name = dist_info['metadata']['name']
    version = wheel_metadata['version']

    artifact_id = package_name.replace('-', '_')
    if not group_id:
        group_id = artifact_id

    udf_reqs = [f'{package_name}=={version}']  # TODO: extend with optional extras udf section
    classes = []
    for display_name, fn_metadata in entry_points.items():
        py_fn_name = fn_metadata["attr"]
        source_code = f'from {fn_metadata["module"]} import {py_fn_name}'
        exec(source_code)
        py_fn = eval(py_fn_name)
        type_hints = get_type_hints(py_fn)
        return_annotation_key = 'return'
        assert return_annotation_key in type_hints, \
            f'{py_fn_name} must have a return type annotated in the form "-> type"'
        return_type = type_hints.pop(return_annotation_key)
        parameters = [UdfParameter(param_name, _python_type_to_ksqldb_type[input_type]) for (param_name, input_type)
                      in type_hints.items()]
        udf_handler = UdfHandler(py_fn_name, parameters, _python_type_to_ksqldb_type[return_type],
                                 _udf_type_to_default_value[return_type])
        udf_class = UdfClass(display_name, source_code, udf_reqs, [udf_handler])
        classes.append(udf_class)
    package = UdfPackage(group_id, artifact_id, version, classes, [wheel_path])
    print(package.build(target_dir))


def main():
    Fire(build_jar_from_wheel)


if __name__ == '__main__':
    main()
