from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from api import plan

from datamodels.plan_model import plan_fields
from datamodels.project_model import project_fields
from datamodels.polygon_model import polygon_fields
import rhino.geometry
import api


class OpenPlansProject:

    _PROJECT_MODEL = project_fields

    def __init__(self, data_fields=_PROJECT_MODEL):
        self.__project = data_fields

    @classmethod
    def from_data(cls, data):
        """Construct a Open Plans Project from its api data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`OpenPlansProject`
            The constructed dataclass.
        """
        return cls(data_fields={k: v for k, v in data.iteritems() if k in OpenPlansProject._PROJECT_MODEL})

    @classmethod
    def from_custom(cls, data={}, **kwargs):
        project_fields = OpenPlansProject._PROJECT_MODEL.copy()
        for key in data:
            project_fields[key] = data[key]
        for key in kwargs:
            project_fields[key] = kwargs[key]
        return cls(data_fields=project_fields)

    @classmethod
    def from_project_id(cls, id):
        return cls.from_data(data=api.get_data(dict=api.fetch_project(project_id=id), key='project'))

    @property
    def project(self):
        return self.__project

    @property
    def plans(self):
        return self.project['plans']

    @property
    def name(self):
        return self.project['name']

    @property
    def project_id(self):
        return self.project['id']

    @property
    def plan_ids(self):
        return [p['id'] for p in self.plans if p['id']]

    def modify_project(self, field_changes={}, **kwargs):
        for key in field_changes:
            self.__project[key] = field_changes[key]
        for key in kwargs:
            self.__project[key] = kwargs[key]
        return self

    def fetch_project_plans(self):
        return [OpenPlansPlan.from_plan_id(id=id) for id in self.plan_ids ]

    @property
    def project_id_string(self):
        return "Name: {}; ID: {}".format(
            self.name, self.project_id)

    def __repr__(self):
        return "{}(project={})".format(self.__class__.__name__, self.project)


class OpenPlansPlan:

    _PLAN_MODEL = plan_fields

    def __init__(self, data_fields=_PLAN_MODEL):
        self.__plan = data_fields

    @classmethod
    def from_data(cls, data):
        """Construct a Open Plans plan from its api data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`OpenPlansPlan`
            The constructed dataclass.
        """
        return cls(data_fields={k: v for k, v in data.iteritems() if k in OpenPlansPlan._PLAN_MODEL})

    @classmethod
    def from_custom(cls, data={}, **kwargs):
        plan_fields = OpenPlansPlan._PROJECT_PLAN.copy()
        for key in data:
            plan_fields[key] = data[key]
        for key in kwargs:
            plan_fields[key] = kwargs[key]
        return cls(data_fields=plan_fields)

    @classmethod
    def from_plan_id(cls, id):
        return cls.from_data(data=api.get_data(dict=api.fetch_plan(plan_id=id), key='plan'))

    @property
    def plan_id(self):
        return self.__plan['id']

    @property
    def floor(self):
        return self.__plan['floor']

    @property
    def plan_id_string(self):
        return "{} Level; ID: {}".format(str(self.floor).zfill(2), self.plan_id)