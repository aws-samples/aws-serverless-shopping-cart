#rappidmq send query to shopping-cart-service
#!/usr/bin/env python3
# Path: backend/shopping-cart-service/rappidmq.py
# Compare this snippet from backend/shopping-cart-service/add_to_cart.py:

def rappidmq_send_query(query, queue_name):
    """
    Send a query to the queue.
    """
    logger.info("Sending query to queue: %s", queue_name)
    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    queue.send_message(MessageBody=query)
    logger.info("Query sent to queue: %s", queue_name)