import docker
client = docker.from_env()

def pull_image(image):
    response = client.api.pull(image, stream=True, decode=True)
    for line in response:
        print(line['status'])

def build_container(image, local_dir, env):
    return client.api.create_container(
        image, 
        command=["tail", "-f", "/dev/null"],
        working_dir='/opt/compliance',
        environment=env,
        host_config=client.api.create_host_config(
            binds={
                local_dir: '/opt/compliance'
            }
        )
    )

def execute_instruction(container, instruction):
    exec_id = client.api.exec_create(container, cmd=["bash", "-c", instruction])
    output = client.api.exec_start(exec_id)
    inspect = client.api.exec_inspect(exec_id)
    return [inspect['ExitCode'], instruction, output]

def execute_steps(image, local_dir, steps, env):
    container = build_container(image, local_dir, env)
    try:
        client.api.start(container=container)

        total_result = []
        for i in steps:
            execute_result = execute_instruction(container, i)
            total_result.append(execute_result)
            if execute_result[0] != 0:
                return (False, total_result)
        
        return (True, total_result)
    finally:
        client.api.kill(container=container)
    
