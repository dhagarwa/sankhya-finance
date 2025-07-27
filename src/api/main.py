"""
Sankhya Finance API - Streaming Financial Analysis
FastAPI application with real-time progress updates through the agentic chain
"""

import asyncio
import json
import os
import traceback
from datetime import datetime
from typing import AsyncGenerator, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our analysis system
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.o3_query_decomposer import O3QueryDecomposer, QueryPatterns

app = FastAPI(
    title="Sankhya Finance API",
    description="AI-Powered Financial Analysis with Real-time Streaming",
    version="1.0.0"
)

# CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the HTML client
app.mount("/static", StaticFiles(directory="src/api/static"), name="static")


class QueryRequest(BaseModel):
    query: str
    debug_mode: bool = False


class StreamingAnalyzer:
    """Enhanced analyzer with streaming capabilities"""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
    
    async def stream_analysis(self, query: str, debug_mode: bool = False) -> AsyncGenerator[str, None]:
        """
        Stream the analysis process with real-time updates
        """
        try:
            # Initial status
            yield self._format_stream_message("status", {
                "stage": "initialization",
                "message": "🚀 Starting Sankhya Finance Analysis",
                "query": query,
                "timestamp": datetime.now().isoformat()
            })
            
            # Check API key
            if not self.openai_api_key or "placeholder" in self.openai_api_key:
                yield self._format_stream_message("error", {
                    "message": "❌ Missing OpenAI API key - Analysis cannot proceed",
                    "timestamp": datetime.now().isoformat()
                })
                return
            
            # Pattern analysis
            yield self._format_stream_message("status", {
                "stage": "pattern_analysis",
                "message": "📊 Analyzing query patterns...",
                "timestamp": datetime.now().isoformat()
            })
            
            query_type = QueryPatterns.detect_query_type(query)
            tickers = QueryPatterns.extract_tickers(query)
            
            yield self._format_stream_message("pattern_result", {
                "query_type": query_type,
                "detected_tickers": tickers if tickers else [],
                "message": f"🔍 Detected query type: {query_type}",
                "timestamp": datetime.now().isoformat()
            })
            
            # Start decomposition
            yield self._format_stream_message("status", {
                "stage": "decomposition",
                "message": "🧠 Starting O3 reasoning and query decomposition...",
                "timestamp": datetime.now().isoformat()
            })
            
            async with O3QueryDecomposer(self.openai_api_key) as decomposer:
                # Get initial decomposition
                decomposition = await decomposer._initial_decomposition(query, debug_mode)
                
                yield self._format_stream_message("decomposition_result", {
                    "reasoning": decomposition.reasoning,
                    "steps_count": len(decomposition.steps),
                    "steps": [
                        {
                            "step_id": step.step_id,
                            "description": step.description,
                            "step_type": step.step_type
                        } for step in decomposition.steps
                    ],
                    "message": f"📝 Generated {len(decomposition.steps)} execution steps",
                    "timestamp": datetime.now().isoformat()
                })
                
                # Refinement
                yield self._format_stream_message("status", {
                    "stage": "refinement",
                    "message": "🔄 Refining decomposition and validating steps...",
                    "timestamp": datetime.now().isoformat()
                })
                
                refined_decomposition = await decomposer._iterative_refinement(decomposition, debug_mode)
                
                # Execution with step-by-step streaming
                yield self._format_stream_message("status", {
                    "stage": "execution",
                    "message": "🚀 Beginning step execution...",
                    "timestamp": datetime.now().isoformat()
                })
                
                executed_steps = {}
                
                for step in refined_decomposition.steps:
                    if step.status == "failed":
                        yield self._format_stream_message("step_failed", {
                            "step_id": step.step_id,
                            "error": step.error,
                            "message": f"❌ Step {step.step_id} failed during validation",
                            "timestamp": datetime.now().isoformat()
                        })
                        continue
                    
                    # Check dependencies
                    dependencies_ready = all(
                        dep_id in executed_steps and executed_steps[dep_id].status == "completed"
                        for dep_id in step.depends_on
                    )
                    
                    if not dependencies_ready:
                        step.status = "failed"
                        step.error = "Dependencies not satisfied"
                        yield self._format_stream_message("step_failed", {
                            "step_id": step.step_id,
                            "error": step.error,
                            "message": f"❌ Step {step.step_id} failed: dependencies not satisfied",
                            "timestamp": datetime.now().isoformat()
                        })
                        continue
                    
                    # Start step execution
                    step.status = "in_progress"
                    yield self._format_stream_message("step_start", {
                        "step_id": step.step_id,
                        "step_type": step.step_type,
                        "description": step.description,
                        "message": f"🔧 Executing {step.step_id} ({step.step_type}): {step.description}",
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    try:
                        if step.step_type == "DATA":
                            await decomposer._execute_data_step(step, debug_mode)
                        elif step.step_type == "ANALYSIS":
                            yield self._format_stream_message("step_progress", {
                                "step_id": step.step_id,
                                "message": "🧠 Running GPT-4o analysis...",
                                "timestamp": datetime.now().isoformat()
                            })
                            await decomposer._execute_analysis_step(step, executed_steps, debug_mode)
                        elif step.step_type == "OUTPUT":
                            yield self._format_stream_message("step_progress", {
                                "step_id": step.step_id,
                                "message": "🎨 Formatting output...",
                                "timestamp": datetime.now().isoformat()
                            })
                            await decomposer._execute_output_step(step, executed_steps, debug_mode)
                        
                        if step.status == "completed":
                            yield self._format_stream_message("step_completed", {
                                "step_id": step.step_id,
                                "step_type": step.step_type,
                                "message": f"✅ {step.step_id} completed successfully",
                                "result_preview": str(step.result)[:200] + "..." if step.result and len(str(step.result)) > 200 else str(step.result),
                                "timestamp": datetime.now().isoformat()
                            })
                            
                            # If this is an OUTPUT step, stream the formatted result
                            if step.step_type == "OUTPUT":
                                yield self._format_stream_message("formatted_output", {
                                    "step_id": step.step_id,
                                    "output": step.result,
                                    "timestamp": datetime.now().isoformat()
                                })
                        
                    except Exception as e:
                        step.status = "failed"
                        step.error = str(e)
                        yield self._format_stream_message("step_failed", {
                            "step_id": step.step_id,
                            "error": step.error,
                            "message": f"❌ {step.step_id} failed: {step.error}",
                            "timestamp": datetime.now().isoformat()
                        })
                    
                    executed_steps[step.step_id] = step
                
                # Final summary
                final_analysis = await decomposer._generate_final_analysis(refined_decomposition)
                
                successful_steps = [s for s in refined_decomposition.steps if s.status == "completed"]
                failed_steps = [s for s in refined_decomposition.steps if s.status == "failed"]
                
                yield self._format_stream_message("final_summary", {
                    "status": "completed" if not failed_steps else "partially_completed",
                    "successful_steps": len(successful_steps),
                    "failed_steps": len(failed_steps),
                    "final_analysis": final_analysis,
                    "message": "🎉 Analysis completed!" if not failed_steps else f"⚠️ Analysis completed with {len(failed_steps)} failed steps",
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            yield self._format_stream_message("error", {
                "message": f"❌ System error: {str(e)}",
                "traceback": traceback.format_exc() if debug_mode else None,
                "timestamp": datetime.now().isoformat()
            })
    
    def _format_stream_message(self, message_type: str, data: Dict[str, Any]) -> str:
        """Format message for server-sent events"""
        message = {
            "type": message_type,
            "data": data
        }
        return f"data: {json.dumps(message)}\n\n"


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Sankhya Finance API",
        "status": "healthy",
        "version": "1.0.0",
        "description": "AI-Powered Financial Analysis with Real-time Streaming"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    openai_key = os.getenv("OPENAI_API_KEY")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai_configured": bool(openai_key and "placeholder" not in openai_key),
        "environment": "production" if os.getenv("ENV") == "production" else "development"
    }


@app.post("/analyze")
async def analyze_query(request: QueryRequest):
    """
    Analyze a financial query with streaming real-time updates
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key or "placeholder" in openai_api_key:
        raise HTTPException(
            status_code=400, 
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    analyzer = StreamingAnalyzer(openai_api_key)
    
    return StreamingResponse(
        analyzer.stream_analysis(request.query, request.debug_mode),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@app.post("/analyze-simple")
async def analyze_simple(request: QueryRequest):
    """
    Simple non-streaming analysis endpoint
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key or "placeholder" in openai_api_key:
        raise HTTPException(
            status_code=400, 
            detail="OpenAI API key not configured"
        )
    
    try:
        # Import the original analysis function
        from main import analyze_financial_query
        
        result = await analyze_financial_query(request.query, request.debug_mode)
        
        return {
            "success": True,
            "query": request.query,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("ENV") != "production"
    ) 