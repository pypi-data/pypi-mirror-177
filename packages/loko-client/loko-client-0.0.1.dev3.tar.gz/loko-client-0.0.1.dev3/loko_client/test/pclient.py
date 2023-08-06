import time

from loko_client.business.projects_client import AsyncProjectsClient, ProjectsClient
import asyncio

GATEWAY = 'http://localhost:9999/routes/'

async_client = False
pclient = AsyncProjectsClient(gateway=GATEWAY) if async_client else ProjectsClient(gateway=GATEWAY)

async def test(pclient):

    print(pclient)

    ### PROJECTS ###
    if async_client:
        print(f'ALL PROJECTS: {await pclient.all_projects()}')
    else:
        print(f'ALL PROJECTS: {pclient.all_projects()}')
    if async_client:
        prj = await pclient.get_project("hello")
    else:
        prj = pclient.get_project("hello")
    print(f'ALL TABS: {prj.tabs.all()}')
    all_nodes = []
    for tab in prj.tabs.all():
        all_nodes += prj.tabs[tab].nodes.nodes.values()
    print(f'ALL NODES: {all_nodes}')
    print(f'ALL NODES IDS: {[node.id for node in all_nodes]}')

    nodes = prj.tabs.main.nodes
    print(f'ALL MAIN NODES IDS: {nodes.all()}')
    print(f'ALL MAIN NODES: {nodes.nodes}')

    res = prj.tabs.main.nodes.search('data.name', 'HTTP Request')
    print(f'SEARCH FOR HTTP Request: {list(res)}')
    for node_id in res:
        node = prj.tabs.main.nodes[node_id]
        print(node.to_dict())
        print(node.data['name'])

    res = prj.tabs.main.nodes.search('data.options.values.alias', 'prova')
    print(f'SEARCH FOR alias=prova: {list(res)}')
    for node_id in res:
        node = prj.tabs.main.nodes[node_id]
        print(node.to_dict())
        print(node.data['options']['values']['alias'])

    ### TASKS ###
    if async_client:
        running = await pclient.running_tasks()
    else:
        running = pclient.running_tasks()
    print(f'RUNNING: {running}')
    for task in running:
        print(task)
        print(f'project: {task["project"]} - tab: {task["graph"]} - node_name: {task["source"]} - '
              f'uid: {task["uid"]} - user: {task["user"]} - started: {task["startedAt"]}')
    if running:
        print(f'CANCEL TASK: project {running[0]["project"]} - tab {running[0]["graph"]} - uid {running[0]["uid"]}')
        if async_client:
            print(await pclient.cancel_task(uid=running[0]['uid']))
            print(f'RUNNING: {await pclient.running_tasks()}')
        else:
            print(pclient.cancel_task(uid=running[0]['uid']))
            print(f'RUNNING: {pclient.running_tasks()}')
    time.sleep(1)
    if async_client:
        trigger_id = list((await pclient.get_project('hello')).tabs.main.nodes.search('data.name', 'Trigger'))[0]
        await pclient.trigger('hello', trigger_id)
    else:
        trigger_id = list(pclient.get_project('hello').tabs.main.nodes.search('data.name', 'Trigger'))[0]
        pclient.trigger('hello', trigger_id)
    if async_client:
        print(f'RUNNING: {await pclient.running_tasks()}')
        print(f'DEPLOYMENT STATUS {await pclient.deployment_status("hello")}')
        print(await pclient.undeploy('hello'))
        print(f'DEPLOYMENT STATUS {await pclient.deployment_status("hello")}')
        print(await pclient.deploy('hello'))
        print(f'DEPLOYMENT STATUS {await pclient.deployment_status("hello")}')
    else:
        print(f'RUNNING: {pclient.running_tasks()}')
        print(f'DEPLOYMENT STATUS {pclient.deployment_status("hello")}')
        print(pclient.undeploy('hello'))
        print(f'DEPLOYMENT STATUS {pclient.deployment_status("hello")}')
        print(pclient.deploy('hello'))
        print(f'DEPLOYMENT STATUS {pclient.deployment_status("hello")}')


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(test(pclient))
r = loop.run_until_complete(task)