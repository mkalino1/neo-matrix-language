from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
import io
from contextlib import redirect_stdout
import logging

from language.interpreter.Interpreter import Interpreter
from language.lexer.Lexer import Lexer
from language.parser.Parser import Parser
from language.lexer.Source import SourceString
from language.errors.InterpreterExceptions import NeoRuntimeError
from language.errors.LexerExceptions import LexerError
from language.errors.ParserExceptions import EmptyMatrix, InvalidMatrix, InvalidSyntax
from language.limits import (
    MAX_API_CODE_LENGTH,
    MAX_API_EXECUTION_STEPS,
    MAX_API_OUTPUT_LENGTH,
    MAX_API_STRING_LENGTH
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Neo Matrix Language Interpreter",
    description="A web interface for executing Neo Matrix Language code",
    version="1.0.0"
)

class CodeRequest(BaseModel):
    code: str = Field(max_length=MAX_API_CODE_LENGTH)

class CodeResponse(BaseModel):
    success: bool
    result: str | None = None
    output: str | None = None
    error: str | None = None


class OutputLimitExceeded(Exception):
    pass


class LimitedStringIO(io.StringIO):
    def write(self, text):
        if self.tell() + len(text) > MAX_API_OUTPUT_LENGTH:
            raise OutputLimitExceeded
        return super().write(text)

@app.get("/api/hello")
async def hello():
    return {"message": "Hello, Neo!"}

@app.post("/api/execute", response_model=CodeResponse)
async def execute_code(request: CodeRequest):
    """Execute Neo Matrix Language code and return results"""
    try:
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="No code provided")
        if len(request.code.encode("utf-8")) > MAX_API_CODE_LENGTH:
            raise HTTPException(
                status_code=413,
                detail=f"Code exceeds the {MAX_API_CODE_LENGTH}-byte limit"
            )

        output_capture = LimitedStringIO()
        try:
            with redirect_stdout(output_capture):
                source = SourceString(request.code)
                lexer = Lexer(source)
                parser = Parser(lexer)
                parsed_program = parser.parse_program()
                interpreter = Interpreter(
                    parsed_program,
                    max_steps=MAX_API_EXECUTION_STEPS,
                    max_output_length=MAX_API_OUTPUT_LENGTH,
                    max_string_length=MAX_API_STRING_LENGTH
                )
                succeeded = interpreter.run()

            if not succeeded:
                return CodeResponse(success=False, error=str(interpreter.error))

            return CodeResponse(
                success=True,
                result="None",
                output=output_capture.getvalue()
            )
        except OutputLimitExceeded:
            return CodeResponse(
                success=False,
                error=f"Output exceeds the {MAX_API_OUTPUT_LENGTH}-character limit"
            )
        except (NeoRuntimeError, LexerError, EmptyMatrix, InvalidMatrix, InvalidSyntax) as e:
            return CodeResponse(success=False, error=str(e))
        except Exception as e:
            logger.exception("Unexpected error while executing Neo code")
            return CodeResponse(success=False, error="Internal execution error")

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected API error while executing Neo code")
        raise HTTPException(status_code=500, detail="Internal server error") from e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
