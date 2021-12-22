from dataclasses.Dataclass import Dataclass

class Project(Dataclass):
    def __init__(self, dict):
        super(Project, self).__init__(dict)
        project_id = "",
        name = "",
        description = "",
        civil_engineer = "",
        architects = [],
        source = "",
        year_of_completion = "",
        client = "",
        floors = None,
        height = None,
        floor_area = None,
        floor_area = None,
        plans = [],
        tags = []

