from loko_client.business.base_client import OrchestratorClient, AsyncOrchestratorClient
from loko_client.model.projects import Project


class ProjectsClient(OrchestratorClient):
    """
        Orchestrator client used to manage Loko projects.

        Args:
            gateway (str): Gateway URL.
    """

    def all_projects(self):
        """
            Return Loko projects.

        """
        r = self.u.projects.get()
        return r.json()

    def get_project(self, id: str):
        """
            Return Loko project.

            Args:
                id (str): Loko project id.

            Returns:
                Project: Loko project.

        """
        r = self.u.projects[id].get()
        return Project(**r.json())

    def running_tasks(self):
        """
            Return Loko running tasks.

            Example:
                >>> GATEWAY = 'http://localhost:9999/routes/'
                >>> pclient = ProjectsClient(gateway=GATEWAY)
                >>> running = pclient.running_tasks()
                >>> for task in running:
                >>>     print(f'project: {task["project"]} - tab: {task["graph"]} - node_name: {task["source"]} - '
                >>>     f'uid: {task["uid"]} - user: {task["user"]} - started: {task["startedAt"]}')

            Returns:
                List[dict]: List of dictionaries containing information of running tasks.
        """
        r = self.u.tasks.get()
        return r.json()

    def cancel_all_tasks(self):
        """ Cancel all Loko running tasks. """
        r = self.u.tasks.delete()
        return r.json()

    def cancel_task(self, uid: str):
        """
            Cancel a single Loko task using its uid.

            Example:
                >>> GATEWAY = 'http://localhost:9999/routes/'
                >>> pclient = ProjectsClient(gateway=GATEWAY)
                >>> running = pclient.running_tasks()
                >>> print(f'RUNNING: {running}')
                >>> if running:
                >>>     print(f'CANCEL TASK: project {running[0]["project"]} - tab {running[0]["graph"]} - uid {running[0]["uid"]}')
                >>>     print(pclient.cancel_task(uid=running[0]['uid']))
                >>>     print(f'RUNNING: {pclient.running_tasks()}')

            Args:
                uid (str): Loko task uid.
        """
        r = self.u.tasks[uid].delete()
        return r.json()

    def trigger(self, project_id: str, component_id: str):
        """
            Start Loko task using *project_id* and *component_id*.

            Example:
                >>> GATEWAY = 'http://localhost:9999/routes/'
                >>> pclient = ProjectsClient(gateway=GATEWAY)
                >>> component_id = list(pclient.get_project('first_project').tabs.main.nodes.search('data.options.values.alias',
                >>>                                                                                 'My block'))[0]
                >>> pclient.trigger('first_project', component_id)
                >>> print(pclient.running_tasks())

            Args:
                project_id (str): Loko project id.
                component_id (str): Loko node id.

        """
        r = self.u.projects[project_id].trigger.post(json=dict(id=component_id))
        return r.json()

    def deploy(self, project_id: str):
        """
            Deploy Loko project.

            Args:
                project_id (str): Loko project id.
        """
        r = self.u.deploy[project_id].get()
        return r.json()

    def undeploy(self, project_id: str):
        """
            Undeploy Loko project.

            Args:
                project_id (str): Loko project id.
        """
        r = self.u.undeploy[project_id].get()
        return r.json()

    def deployment_status(self, project_id: str):
        """
            Check Loko project's deployment status.

            Args:
                project_id (str): Loko project id.

            Returns:
                dict: Dictionary containing project `status` and associated `guis`.
        """
        r = self.u.deployment_status[project_id].get()
        return r.json()


class AsyncProjectsClient(AsyncOrchestratorClient):
    """
        Orchestrator client used to manage Loko projects.

        Args:
            gateway (str): Gateway URL.
            timeout (float): The maximal number of seconds for the whole operation including connection establishment,
                request sending and response reading. Default: 300
    """

    async def all_projects(self):
        """
            Return Loko projects.

        """
        r = await self.u.projects.request('GET')
        return await r.json()

    async def get_project(self, id: str):
        """
            Return Loko project.

            Args:
                id (str): Loko project id.

            Returns:
                Project: Loko project.

        """
        r = await self.u.projects[id].request('GET')
        return Project(** await r.json())

    async def running_tasks(self):
        """
            Return Loko running tasks.

            Example:
                >>> GATEWAY = 'http://localhost:9999/routes/'
                >>> pclient = ProjectsClient(gateway=GATEWAY)
                >>> running = await pclient.running_tasks()
                >>> for task in running:
                >>>     print(f'project: {task["project"]} - tab: {task["graph"]} - node_name: {task["source"]} - '
                >>>     f'uid: {task["uid"]} - user: {task["user"]} - started: {task["startedAt"]}')

            Returns:
                List[dict]: List of dictionaries containing information of running tasks.
        """
        r = await self.u.tasks.request('GET')
        return await r.json()

    async def cancel_all_tasks(self):
        """ Cancel all Loko running tasks. """
        r = await self.u.tasks.request('DELETE')
        return await r.json()

    async def cancel_task(self, uid: str):
        """
            Cancel a single Loko task using its uid.

            Example:
                >>> GATEWAY = 'http://localhost:9999/routes/'
                >>> pclient = ProjectsClient(gateway=GATEWAY)
                >>> running = await pclient.running_tasks()
                >>> print(f'RUNNING: {running}')
                >>> if running:
                >>>     print(f'CANCEL TASK: project {running[0]["project"]} - tab {running[0]["graph"]} - uid {running[0]["uid"]}')
                >>>     print(await pclient.cancel_task(uid=running[0]['uid']))
                >>>     print(f'RUNNING: {await pclient.running_tasks()}')

            Args:
                uid (str): Loko task uid.
        """
        r = await self.u.tasks[uid].request('DELETE')
        return await r.json()

    async def trigger(self, project_id: str, component_id: str):
        """
            Start Loko task using *project_id* and *component_id*.

            Example:
                >>> GATEWAY = 'http://localhost:9999/routes/'
                >>> pclient = ProjectsClient(gateway=GATEWAY)
                >>> prj = await pclient.get_project("first_project")
                >>> component_id = list(prj.tabs.main.nodes.search('data.options.values.alias',
                >>>                                                'My block'))[0]
                >>> pclient.trigger('first_project', component_id)
                >>> print(pclient.running_tasks())

            Args:
                project_id (str): Loko project id.
                component_id (str): Loko node id.

        """
        r = await self.u.projects[project_id].trigger.request('POST', json=dict(id=component_id))
        return await r.json()

    async def deploy(self, project_id: str):
        """
            Deploy Loko project.

            Args:
                project_id (str): Loko project id.
        """
        r = await self.u.deploy[project_id].request('GET')
        return await r.json()

    async def undeploy(self, project_id: str):
        """
            Undeploy Loko project.

            Args:
                project_id (str): Loko project id.
        """
        r = await self.u.undeploy[project_id].request('GET')
        return await r.json()

    async def deployment_status(self, project_id: str):
        """
            Check Loko project's deployment status.

            Args:
                project_id (str): Loko project id.

            Returns:
                dict: Dictionary containing project `status` and associated `guis`.
        """
        r = await self.u.deployment_status[project_id].request('GET')
        return await r.json()
