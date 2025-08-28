from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import io
from contextlib import redirect_stdout
import traceback

from Interpreter.Interpreter import Interpreter
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Lexer.Source import SourceString

app = FastAPI(
    title="Neo Matrix Language Interpreter",
    description="A web interface for executing Neo Matrix Language code",
    version="1.0.0"
)

class CodeRequest(BaseModel):
    code: str

class CodeResponse(BaseModel):
    success: bool
    result: str | None = None
    output: str | None = None
    error: str | None = None
    traceback: str | None = None

@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the main page"""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Neo Matrix Language Interpreter</h1><p>Template not found</p>")

@app.post("/execute", response_model=CodeResponse)
async def execute_code(request: CodeRequest):
    """Execute Neo Matrix Language code and return results"""
    try:
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="No code provided")
        
        # Capture stdout to get print output
        output_capture = io.StringIO()
        
        try:
            with redirect_stdout(output_capture):
                source = SourceString(request.code)
                lexer = Lexer(source)
                parser = Parser(lexer)
                parsed_program = parser.parse_program()
                interpreter = Interpreter(parsed_program)
                result = interpreter.run()
            
            captured_output = output_capture.getvalue()
            
            return CodeResponse(
                success=True,
                result=str(result) if result is not None else "None",
                output=captured_output
            )
            
        except Exception as e:
            error_info = traceback.format_exc()
            return CodeResponse(
                success=False,
                error=str(e),
                traceback=error_info
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)

