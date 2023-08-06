from abc import ABC as ABSTRACT_BASE_CLASS
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from shutil import rmtree as delete_dir
from string import Template
from typing import List, Any, ClassVar, Union

from ksqldb_udf import run_command


class JavaType(Enum):
    byte = auto()
    short = auto()
    int = auto()
    long = auto()
    float = auto()
    double = auto()
    boolean = auto()
    char = auto()
    String = auto()
    BigDecimal = auto()


_ksql_supported_types = [(type.name, type.value) for type in
                         (JavaType.int, JavaType.long, JavaType.double, JavaType.String, JavaType.boolean,
                          JavaType.BigDecimal)]
_ksql_supported_types.append(('bytes', auto()))
KsqldbUdfTypes = Enum('KsqldbUdfTypes',
                      _ksql_supported_types)

unimplemented_udf_types = {KsqldbUdfTypes.int, KsqldbUdfTypes.BigDecimal, KsqldbUdfTypes.bytes}

java_type_to_sql_type = {java_type: java_type.name for java_type in
                         (KsqldbUdfTypes.int, KsqldbUdfTypes.double, KsqldbUdfTypes.boolean, KsqldbUdfTypes.String)}
java_type_to_sql_type[KsqldbUdfTypes.long] = 'BIGINT'
java_type_to_sql_type[KsqldbUdfTypes.BigDecimal] = 'DECIMAL'


@dataclass
class UdfParameter:
    name: str
    type: KsqldbUdfTypes

    def __post_init__(self):
        if self.type in unimplemented_udf_types:
            raise NotImplementedError(self.type)

    def __repr__(self):
        return f'@UdfParameter(value="{self.name}") final {self.type.name} {self.name}'

    __str__ = __repr__


@dataclass
class UdfHandler(ABSTRACT_BASE_CLASS):
    py_fn_name: str
    params: List[UdfParameter]
    return_type: KsqldbUdfTypes
    error_value: Any
    description: str = ''
    schema: str = ''
    schema_provider: str = ''

    def __post_init__(self):
        if self.return_type in unimplemented_udf_types:
            raise NotImplementedError(self.return_type)
        if self.return_type == KsqldbUdfTypes.String:
            self.error_value = f'"{self.error_value}"'
        elif self.return_type == KsqldbUdfTypes.boolean:
            self.error_value = str(self.error_value).lower()

    def __str__(self):
        template = Template("""
    @Udf(description="$description")
    public $return_type handle($udf_params) {
        try (PythonInterpreter interpreter = getPythonInstance()) {
            interpreter.exec($code_var_name);
            PyObject udfFn = (PyObject) interpreter.get("$python_fn_name");
            $return_type out = ($return_type) udfFn.invokeMethod("__call__", $udf_args);
            return out;
        } catch (PythonEnvironmentException e) {
            e.printStackTrace();
            return $error_value;
        }
    }
    """)
        param_str = ', '.join(str(param) for param in self.params)
        arg_str = ', '.join([param.name for param in self.params])
        return template.substitute(description=self.description,
                                   udf_params=param_str,
                                   python_fn_name=self.py_fn_name,
                                   return_type=self.return_type.name,
                                   udf_args=arg_str,
                                   error_value=self.error_value,
                                   code_var_name=UdfClass.code_var_name)


@dataclass
class UdfClass:
    display_name: str
    udf_code: str
    python_requirements: List[str]
    udf_handlers: List[UdfHandler]
    configure_code: str = ""
    description: str = ""
    author: str = ""
    version: str = ""

    code_var_name: ClassVar[str] = 'udfCode'

    @staticmethod
    def _encode_python_code(code: str):
        return code.encode('unicode_escape').decode('utf-8').replace('"', r'\"')

    def __post_init__(self):
        self.udf_code = self._encode_python_code(self.udf_code)
        self.configure_code = self._encode_python_code(self.configure_code)
        self.python_requirements = deepcopy(self.python_requirements)
        self.python_requirements.append('pemja==0.2.*')

    def build(self, package_name: str, out_dir: Path):
        udf_java_code = f'package {package_name};\n{str(self)}'
        (out_dir / f'{self.display_name}.java').write_text(udf_java_code)

    def __str__(self):
        template = Template("""
import io.confluent.csid.ksqldb.udf.PythonUdf;
import io.confluent.csid.python.environment.PythonEnvironmentException;
import io.confluent.ksql.function.udf.Udf;
import io.confluent.ksql.function.udf.UdfDescription;
import io.confluent.ksql.function.udf.UdfParameter;
import pemja.core.PythonInterpreter;
import pemja.core.object.PyObject;

import java.util.Map;

@UdfDescription(name="$display_name", description="$udf_description")
public class $display_name extends PythonUdf {
    private static String configureCode = "$configure_code";
    private static String $code_var_name = "$udf_code";
    private static String[] pythonRequirements = new String[] {$python_requirements};

    public $display_name() {
        super(pythonRequirements, "$display_name");
    }

    @Override
    public void configure(final Map<String, ?> map) {
        super.configure(map);
        if (configureCode != "") {
            try (PythonInterpreter interpreter = getPythonInstance()) {
                interpreter.exec(configureCode);
            } catch (PythonEnvironmentException e) {
                e.printStackTrace();
            }
        }
    }

    $udf_handlers
}
""")
        python_requirements = '", "'.join(self.python_requirements)
        python_requirements = f'"{python_requirements}"'
        udf_handlers = '\n'.join(str(handler) for handler in self.udf_handlers)
        return template.substitute(
            display_name=self.display_name,
            udf_description=self.description,
            configure_code=self.configure_code,
            code_var_name=self.code_var_name,
            udf_code=self.udf_code,
            python_requirements=python_requirements,
            udf_handlers=udf_handlers
        )


class UdfJavaLib:
    def __init__(self):
        self._group_id = 'io.confluent.csid'
        self._artifact_id = 'ksqldb-udf'
        self._version = '0.1.0-SNAPSHOT'

    def install(self, install_dir: Path):
        project_dir = Path(__file__).parent
        local_maven_repo_name = "local-maven-repo"
        jar_glob_pattern = 'ksqldb-udf-python-core-[0-9].[0-9].[0-9]*-jar-with-dependencies.jar'
        java_udf_lib_jar = next(project_dir.glob(jar_glob_pattern))
        run_command('mvn',
                    'deploy:deploy-file',
                    f'-DgroupId={self._group_id}',
                    f'-DartifactId={self._artifact_id}',
                    f'-Dversion={self._version}',
                    f'-Durl=file:{str(install_dir / local_maven_repo_name)}',
                    f'-DrepositoryId={local_maven_repo_name}',
                    '-DupdateReleaseInfo=true',
                    f'-Dfile={str(java_udf_lib_jar)}')


class UdfPackage:
    def __init__(self, group_id: str, artifact_id: str, version: str, udf_classes: Union[UdfClass, List[UdfClass]],
                 local_dependencies: List[Path] = []):
        self._group_id = group_id
        self._artifact_id = artifact_id
        self._version = version
        self._udf_classes = [udf_classes] if isinstance(udf_classes, UdfClass) else udf_classes
        self._local_dependencies = local_dependencies

        self._package_dir = Path(__file__).parent
        self._build_dir = self._package_dir.parent / 'build'

    def build(self, target_dir: Path = None) -> Path:
        self._build_dir.mkdir(parents=True, exist_ok=True)
        try:
            pom_template = Template((self._package_dir / 'pom-template.xml').read_text())
            pom = pom_template.substitute(group_id=self._group_id,
                                          artifact_id=self._artifact_id,
                                          package_version=self._version,
                                          ksqldb_udf_lib_version='0.1.0-SNAPSHOT')
            (self._build_dir / 'pom.xml').write_text(pom)

            java_project_dir = self._build_dir / 'src/main'
            code_dir = java_project_dir / 'java' / self._group_id.replace('.', '/')
            code_dir.mkdir(parents=True, exist_ok=True)
            for udf_class in self._udf_classes:
                udf_class.build(self._group_id, code_dir)
            if self._local_dependencies:
                wheel_dir = java_project_dir / 'resources' / 'python-dependencies'
                wheel_dir.mkdir(parents=True, exist_ok=True)
                for local_dependency in self._local_dependencies:
                    wheel_dir.joinpath(local_dependency.name).write_bytes(local_dependency.read_bytes())

            UdfJavaLib().install(self._build_dir)
            run_command('mvn', 'clean', 'package', '-f', str(self._build_dir))
            udf_jar_path = self._build_dir / f'target/{self._artifact_id}-{self._version}.jar'
            assert udf_jar_path.exists()
            if target_dir is None:
                target_dir = Path().cwd()
            output_path = target_dir / udf_jar_path.name
            udf_jar_path.rename(output_path)
        finally:
            delete_dir(self._build_dir)
        return output_path
