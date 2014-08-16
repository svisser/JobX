import collections

import mr.handlers.source
import mr.handlers.library
import mr.handlers.general

_MANAGED_WORKFLOW_CLS = collections.namedtuple(
                            'ManagedWorkflow', 
                            ['workflow', 'handlers'])


class _WorkflowManager(object):
    def __init__(self):
        self.__workflows = {}

    def add(self, workflow):
        if workflow.workflow_name in self.__workflows:
            raise ValueError("Workflow already registered: [%s]" % 
                             (workflow.workflow_name,))

# TODO(dustin): Make these configurable (they implement an interface).
        s = mr.handlers.source.FilesystemSourceAdapter(workflow)
        l = mr.handlers.library.KvLibraryAdapter(workflow)

        h = mr.handlers.general.Handlers(s, l)

        self.__workflows[workflow.workflow_name] = _MANAGED_WORKFLOW_CLS(
                                                    workflow=workflow, 
                                                    handlers=h)

    def get(self, workflow_name):
        return self.__workflows[workflow_name]

_wm = _WorkflowManager()

def get_wm():
    return _wm