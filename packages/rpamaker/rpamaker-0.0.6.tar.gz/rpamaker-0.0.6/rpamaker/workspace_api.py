import datetime
import logging
from datetime import datetime
from multiprocessing import Process

import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from .utils import get_base_path, call_robot


def start_workspace_api():
    app = FastAPI()

    @app.get("/")
    def test_endpoint():
        return JSONResponse(content={'status': 'ok'}, status_code=200)

    @app.get("/test")
    def test_file():
        file_location = get_base_path()

        return {"path": file_location}

    @app.post("/run/{keyword}/{t_id}/{w_id}/")
    async def run_robot(request: Request, keyword, t_id, w_id, background_tasks: BackgroundTasks):
        logging.debug(f'{datetime.now()}')

        console_flag = request.headers.get('console_flag') == 'True'

        json_body = {}
        try:
            json_body = await request.json()
        except Exception as err:
            logging.error(err)

        variables = []
        for k, v in json_body.items():
            variables.append('--variable')
            variables.append(f'{k}:{v}')

        variables.extend([
            '--variable', f'id_t:{t_id}',
            '--variable', f'id_p:{w_id}',
            '--variable', f'console_flag:{console_flag}',
        ])

        start_process(keyword, variables, t_id)

        return 200

    def start_process(keyword, variables, t_id):
        p = Process(target=call_robot, args=(keyword, variables, t_id))
        p.start()
        logging.info(f"Process {p} started")

    logging.info('About to start worksapce')
    uvicorn.run(app, host="127.0.0.1", port=81)


if __name__ == '__main__':
    start_workspace_api()
