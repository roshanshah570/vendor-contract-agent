import asyncio
import json
from google.adk.runners import Runner
from app.app_utils import services
from app.agent import app as adk_app
from google.adk.types import Content

async def main():
    runner = Runner(
        app=adk_app,
        session_service=services.get_session_service(),
        artifact_service=services.get_artifact_service(),
        auto_create_session=True,
    )
    
    event_data = {
        "text": "Dear customer, your Enterprise account will renew for $10,000/Year. Your current usage is only 5 seats. Cancellation requires 60 days notice."
    }
    
    print("Running workflow...")
    # 3. Call runner.run
    content = Content(role="user", parts=[json.dumps({"data": event_data})])
    for event in runner.run(
        user_id="local-test-sub",
        session_id="test-local-123",
        new_message=content,
    ):
        print("Emitted event type:", type(event))
        print("Emitted event:", event)

if __name__ == "__main__":
    asyncio.run(main())
