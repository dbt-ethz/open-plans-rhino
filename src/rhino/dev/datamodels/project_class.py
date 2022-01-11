from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from datamodels.plan_model import plan_fields
from datamodels.project_model import project_fields
from datamodels.polygon_model import polygon_fields
import api


class OpenPlansProject:

    _PROJECT_MODEL = project_fields

    def __init__(self, project=None):
        self.__project = project if project else OpenPlansProject._PROJECT_MODEL
        self.__plans = [self.PlanData(plan=p) for p in self.__project['plans']]

    @property
    def project(self):
        return self.__project

    @property
    def plans(self):
        return [p.plan for p in self.__plans]

    @property
    def name(self):
        return self.project['name']

    @property
    def project_id(self):
        return self.project['id']

    @property
    def plan_ids(self):
        return [p['id'] for p in self.plans if p['id']]

    @property
    def num_of_plans(self):
        return len(self.plan_ids)

    def add_plan(self, plan):
        self.__plans.append(self.PlanData(plan=plan))
        self.__project['plans'] = self.plans
        return self

    def modify_project(self, field_changes={}, **kwargs):
        for key in field_changes:
            self.__project[key] = field_changes[key]
        for key in kwargs:
            self.__project[key] = kwargs[key]
        return self

    def project_id_string(self):
        return "ID: {}; Name: {}".format(
            self.project_id, self.name)

    def __repr__(self):
        return "{}(project={})".format(self.__class__.__name__, self.project)


    class PlanData:

        _PLAN_MODEL = plan_fields

        def __init__(self, plan):
            self.__plan = plan

        @property
        def plan(self):
            return self.__plan

        @property
        def floor(self):
            return self.plan['floor']

        class PolygonData:

            _POLYGON_MODEL = polygon_fields

            def __init__(self, polygon):
                self.__polygon = polygon
