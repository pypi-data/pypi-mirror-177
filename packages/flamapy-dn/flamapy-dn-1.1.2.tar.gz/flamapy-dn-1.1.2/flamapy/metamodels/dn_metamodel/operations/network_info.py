from flamapy.core.operations import Operation

from flamapy.metamodels.dn_metamodel.models import DependencyNetwork, RequirementFile, Version


class NetworkInfo(Operation):

    def __init__(self) -> None:
        self.result: dict[str, int] = {
            'direct_dependencies': 0,
            'indirect_dependencies': 0,
            'direct_cves': 0,
            'indirect_cves': 0,
            'constraints': 0
        }
        self.direct_dependencies: list[str] = []
        self.indirect_dependencies: list[str] = []
        self.direct_cves: list[str] = []
        self.indirect_cves: list[str] = []

    def get_result(self) -> dict[str, int]:
        return self.result

    def execute(self, model: DependencyNetwork) -> None:
        for requirement_file in model.requirement_files:
            self.search(requirement_file, 'direct')
        self.result['direct_dependencies'] = len(self.direct_dependencies)
        self.result['indirect_dependencies'] = len(self.indirect_dependencies)
        self.result['direct_cves'] = len(self.direct_cves)
        self.result['indirect_cves'] = len(self.indirect_cves)

    def search(self, parent: Version | RequirementFile, level: str) -> None:
        self.result['constraints'] += len(parent.packages)
        for package in parent.packages:
            if (
                package.name not in self.indirect_dependencies and
                package.name not in self.direct_dependencies
            ):
                self.add_dependencie(package.name, level)
            for version in package.versions:
                for cve in version.cves:
                    if (
                        cve['id'] not in self.indirect_cves and 
                        cve['id'] not in self.direct_cves
                    ):
                        self.add_cve(cve['id'], level)
                self.search(version, 'indirect')

    def add_dependencie(self, dependencie_name: str, level: str) -> None:
        match level:
            case 'direct':
                self.direct_dependencies.append(dependencie_name)
            case 'indirect':
                self.indirect_dependencies.append(dependencie_name)

    def add_cve(self, cve_id: str, level: str) -> None:
        match level:
            case 'direct':
                self.direct_cves.append(cve_id)
            case 'indirect':
                self.indirect_cves.append(cve_id)