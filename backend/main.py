from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import tempfile, os, re, json
from datetime import datetime

app = FastAPI(title="AI Resume & Portfolio Builder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Resume & Portfolio Builder API is running"}

# ── Lazy imports so we don't crash on startup ──
def get_modules():
    from resume_generator import generate_pdf_resume, generate_docx_resume
    from nlp_engine import extract_keywords, compute_skill_gap, enhance_bullet_points
    from portfolio_generator import generate_portfolio_html
    return generate_pdf_resume, generate_docx_resume, extract_keywords, compute_skill_gap, enhance_bullet_points, generate_portfolio_html

@app.post("/api/generate-resume/pdf")
def gen_pdf(data: dict):
    gen_pdf_fn, _, _, _, _, _ = get_modules()
    try:
        path = gen_pdf_fn(data)
        name = data.get("personal", {}).get("name", "resume").replace(" ", "_")
        return FileResponse(path, media_type="application/pdf", filename=f"resume_{name}.pdf",
                            headers={"Access-Control-Expose-Headers": "Content-Disposition"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-resume/docx")
def gen_docx(data: dict):
    _, gen_docx_fn, _, _, _, _ = get_modules()
    try:
        path = gen_docx_fn(data)
        name = data.get("personal", {}).get("name", "resume").replace(" ", "_")
        return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            filename=f"resume_{name}.docx",
                            headers={"Access-Control-Expose-Headers": "Content-Disposition"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-job")
def analyze_job(payload: dict):
    _, _, extract_kw, _, _, _ = get_modules()
    try:
        return JSONResponse(content=extract_kw(payload.get("description", "")))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/skill-gap")
def skill_gap(payload: dict):
    _, _, _, compute_gap, _, _ = get_modules()
    try:
        return JSONResponse(content=compute_gap(payload.get("user_skills", []), payload.get("job_description", "")))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enhance-bullets")
def enhance(payload: dict):
    _, _, _, _, enhance_fn, _ = get_modules()
    try:
        return JSONResponse(content={"enhanced": enhance_fn(payload.get("bullets", []), payload.get("role", ""))})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-portfolio-html")
def gen_portfolio(data: dict):
    _, _, _, _, _, port_fn = get_modules()
    try:
        return JSONResponse(content={"html": port_fn(data)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
