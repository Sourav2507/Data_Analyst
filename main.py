from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from agent import run_agent

app = FastAPI()

@app.post("/api/")
async def data_analyst_agent(file: UploadFile = File(...)):
    task_text = (await file.read()).decode("utf-8")
    result, code_info, error = run_agent(task_text)

    if error:
        return JSONResponse(content={
            "error": error,
            "raw_code": code_info.get("raw_code", ""),
            "cleaned_code": code_info.get("cleaned_code", "")
        })

    return JSONResponse(content={
        "result": result,
        "raw_code": code_info.get("raw_code", ""),
        "cleaned_code": code_info.get("cleaned_code", "")
    })
