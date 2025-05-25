from fastapi import APIRouter, HTTPException
from app.schemas import PublishMessageRequest
import json
import pika

router = APIRouter(
     prefix="/notifications",   
)


@router.post("/publish")
def publish_message(payload: PublishMessageRequest):
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Declare queue (make sure the queue exists)
        channel.queue_declare(queue='notification_queue', durable=True)

        # Convert payload to JSON string
        message = json.dumps(payload.dict())

        # Publish message to RabbitMQ
        channel.basic_publish(
            exchange='',
            routing_key='notification_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        connection.close()
        print("Producer endpoint called and message sent to queue:", message) 

        return {"status": "success", "message": "Notification published"}

    except pika.exceptions.AMQPConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to RabbitMQ")

    except Exception as e:
        # Log exception e if you have logging setup
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
