import datetime
import logging
from datetime import datetime
from multiprocessing import Process
from time import sleep

import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from .utils import get_base_path, call_robot


def start_workspace_api():
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.get("/test")
    def test_file():
        file_location = get_base_path()

        return {"path": file_location}

    @app.post("/run/{keyword}/{t_id}/{w_id}/")
    async def run_robot(request: Request, keyword, t_id, w_id, background_tasks: BackgroundTasks):
    # @app.post("/run/{keyword}/")
    # async def run_robot(request: Request, keyword, background_tasks: BackgroundTasks):
        print(f'{datetime.now()}')
        # sleep(5)

        client_host = request.client.host
        console_flag = request.headers.get('console_flag') == 'True'

        json_body = {}
        try:
            json_body = await request.json()
        except Exception as err:
            logging.error(err)
        variables = [f'{k}:{v}' for k, v in json_body.items()]
        variables.extend([
            f'id_t:{t_id}',
            f'id_p:{w_id}',
            f'console_flag:{console_flag}',
        ])

        # background_tasks.add_task(call_robot, keyword,variables)
        p = Process(target=call_robot, args=(keyword, variables))
        p.start()
        print(f"Process {p} started")

        return 200

    print('About to start worksapce')
    uvicorn.run(app, host="127.0.0.1", port=81)


if __name__ == '__main__':
    start_workspace_api()
