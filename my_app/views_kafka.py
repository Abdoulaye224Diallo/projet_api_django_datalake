# my_app/views_kafka.py
import json
import os
import uuid
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from kafka import KafkaProducer


class RepushTransactionView(APIView):
    def post(self, request):
        tx_id = request.data.get("transaction_id")
        if not tx_id:
            return Response({"error": "transaction_id is required"}, status=400)

        for root, _, files in os.walk(os.path.join(settings.BASE_DIR, "data_lake")):
            for f in files:
                if f.endswith(".json"):
                    try:
                        with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                            data = json.load(file)
                            if isinstance(data, dict):
                                data = [data]
                            for tx in data:
                                if tx.get("TRANSACTION_ID") == tx_id:
                                    tx["TIMESTAMP"] = datetime.utcnow().isoformat() + "Z"

                                    producer = KafkaProducer(
                                        bootstrap_servers='localhost:9092',
                                        value_serializer=lambda v: json.dumps(v).encode('utf-8')
                                    )
                                    producer.send("transactions", tx)
                                    producer.flush()
                                    return Response({"message": "Transaction re-pushed to Kafka"})
                    except:
                        continue

        return Response({"error": "Transaction not found"}, status=404)
