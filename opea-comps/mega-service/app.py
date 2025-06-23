import json
import os
import aiohttp
from fastapi import HTTPException, Request
from comps.cores.mega.constants import ServiceType, ServiceRoleType
from comps import MicroService, ServiceOrchestrator
from comps.cores.proto.docarray import LLMParams
from fastapi.responses import StreamingResponse
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo
)

LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 9000)


class ExampleService:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.endpoint = "/v1/example-service"
        self.megaservice = ServiceOrchestrator()
        os.environ["LOGFLAG"] = "true"

    async def check_ollama_connection(self):
        """Check if we can connect to Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{LLM_SERVICE_HOST_IP}:{LLM_SERVICE_PORT}/api/tags"
                async with session.get(url) as response:
                    return response.status == 200
        except Exception:
            return False

    def add_remote_service(self):
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        print(f"Configuring LLM service: http://{LLM_SERVICE_HOST_IP}:{LLM_SERVICE_PORT}{llm.endpoint}")
        self.megaservice.add(llm)

    def start(self):
        self.service = MicroService(
            self.__class__.__name__,
            service_role=ServiceRoleType.MEGASERVICE,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=ChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )

        self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])
        print(f"Service configured with endpoint: {self.endpoint}")
        self.service.start()

    async def handle_request(self, request: Request):
        data = await request.json()
        stream_opt = data.get("stream", True)
        chat_request = ChatCompletionRequest.model_validate(data)

        parameters = LLMParams(
            max_tokens=chat_request.max_tokens or 1024,
            top_k=chat_request.top_k or 10,
            top_p=chat_request.top_p or 0.95,
            temperature=chat_request.temperature or 0.01,
            frequency_penalty=chat_request.frequency_penalty or 0.0,
            presence_penalty=chat_request.presence_penalty or 0.0,
            repetition_penalty=chat_request.repetition_penalty or 1.03,
            stream=stream_opt,
            model=chat_request.model,
            chat_template=chat_request.chat_template,
        )

        initial_inputs = {"messages": chat_request.messages}

        result_dict, runtime_graph = await self.megaservice.schedule(
            initial_inputs=initial_inputs,
            llm_parameters=parameters
        )

        # Check for streaming response first
        for node, response in result_dict.items():
            if isinstance(response, StreamingResponse):
                return response

        # Handle non-streaming response
        last_node = runtime_graph.all_leaves()[-1]

        if last_node not in result_dict:
            raise HTTPException(
                status_code=500,
                detail="No response received from LLM service"
            )

        service_result = result_dict[last_node]

        # Handle OpenAI-style chat completion response format
        if isinstance(service_result, dict):
            if 'choices' in service_result and len(service_result['choices']) > 0:
                message = service_result['choices'][0].get('message', {})
                response = message.get('content', '')
            elif 'error' in service_result:
                error = service_result['error']
                error_msg = error.get('message', 'Unknown error')
                error_type = error.get('type', 'internal_error')
                raise HTTPException(
                    status_code=400 if error_type == 'invalid_request_error' else 500,
                    detail=error_msg
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Unexpected response format from LLM service"
                )
        else:
            response = service_result

        # Return formatted response
        choices = [
            ChatCompletionResponseChoice(
                index=0,
                message=ChatMessage(role="assistant", content=response),
                finish_reason="stop",
            )
        ]
        return ChatCompletionResponse(model="chatqna", choices=choices, usage=UsageInfo())


if __name__ == "__main__":
    example = ExampleService()
    example.add_remote_service()
    example.start()