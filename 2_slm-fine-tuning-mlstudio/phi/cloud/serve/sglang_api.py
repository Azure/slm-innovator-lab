# SGLang and vLLM have their own built-in FastAPI, so this script is not necessary.
# But you can use it as a skeleton code when you need a separate custom implementation for future extensibility.

import os
import subprocess
import threading
import time
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "healthy"}


def run_sglang_server():
    model_path = os.environ.get("MODEL_NAME", "default_model")
    sglang_args = os.environ.get("SGLANG_ARGS", "")
    extra_args = sglang_args.split() if sglang_args else []
    cmd = [
        "python3",
        "-m",
        "sglang.launch_server",
        "--model-path",
        model_path,
    ] + extra_args
    subprocess.run(cmd)


if __name__ == "__main__":
    sglang_thread = threading.Thread(target=run_sglang_server, daemon=True)
    sglang_thread.start()

    # Give the SGLang server some time to start (optional)
    time.sleep(5)

    uvicorn.run(app, host="0.0.0.0", port=30010)
