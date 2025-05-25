import pika, sys, os, json, asyncio, threading
from db import SessionLocal, get_all_fcm_tokens
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
    
cred = credentials.Certificate("./notification-system-ffa63-32d7c97a0923.json")
firebase_admin.initialize_app(cred)

print("Consumer running...")

# Create a new async loop in a separate thread
loop = asyncio.new_event_loop()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, args=(loop,), daemon=True).start()


def send_notification_to_token(token, payload):
    message = messaging.Message(
        notification=messaging.Notification(
            title=payload["title"],
            body=payload["body"],
        ),
        token=token,
    )   
    response = messaging.send(message)
    print('Successfully sent message:', response)

async def fetch_tokens():
    print("Opening DB session...")
    async with SessionLocal() as session:
        tokens = await get_all_fcm_tokens(session)
        print(f"Fetched tokens: {tokens}")
        return tokens

def callback(ch, method, properties, body):
    try:
        payload = json.loads(body)
        print(f"Received payload: {payload}")
        future = asyncio.run_coroutine_threadsafe(fetch_tokens(), loop)
        tokens = future.result()  # This blocks until fetch_tokens completes

        for token in tokens:
            send_notification_to_token(token, payload)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Failed to process message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='notification_queue', durable=True)
    channel.basic_consume(queue='notification_queue', on_message_callback=callback)
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
