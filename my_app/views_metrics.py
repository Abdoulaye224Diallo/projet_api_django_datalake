# views_metrics.py
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MetricsBaseView(APIView):
    def load_all_transactions(self):
        data_lake_dir = os.path.join(settings.BASE_DIR, 'data_lake')
        all_data = []

        for root, _, files in os.walk(data_lake_dir):
            for filename in files:
                if filename.endswith('.json'):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = json.load(f)
                            # Filtrage strict : ne garder que les dicts
                            if isinstance(content, list):
                                all_data.extend([tx for tx in content if isinstance(tx, dict)])
                            elif isinstance(content, dict):
                                all_data.append(content)
                    except Exception as e:
                        print(f"Erreur de lecture {file_path} : {e}")
        return all_data


class SpentLast5MinutesView(MetricsBaseView):
    def get(self, request):
        now = datetime.utcnow()
        five_minutes_ago = now - timedelta(minutes=5)
        total = 0.0

        for transaction in self.load_all_transactions():
            try:
                ts = datetime.fromisoformat(transaction["TIMESTAMP"].replace("Z", "+00:00"))
                if five_minutes_ago <= ts <= now:
                    total += float(transaction.get("AMOUNT", 0.0))
            except Exception as e:
                print(f"Erreur timestamp ou montant : {e}")
                continue

        return Response({"spent_last_5_minutes": round(total, 2)})


class TotalSpentPerUserTransactionView(MetricsBaseView):
    def get(self, request):
        result = defaultdict(lambda: defaultdict(float))

        for tx in self.load_all_transactions():
            if not isinstance(tx, dict):
                continue
            try:
                user = tx.get("USER_ID_HASHED", "unknown")
                t_type = tx.get("TRANSACTION_TYPE", "unknown")
                amount = float(tx.get("AMOUNT", 0.0))
                result[user][t_type] += amount
            except Exception as e:
                print(f"Erreur calcul utilisateur/type : {e}")
                continue

        return Response(result)


class TopProductsView(MetricsBaseView):
    def get(self, request):
        try:
            x = int(request.query_params.get('x', 5))
        except ValueError:
            return Response({"error": "Parameter 'x' must be an integer"}, status=400)

        counter = Counter()

        for tx in self.load_all_transactions():
            if not isinstance(tx, dict):
                continue
            try:
                product = tx.get("PRODUCT_ID", "unknown")
                qty = int(tx.get("QUANTITY", 1))
                counter[product] += qty
            except Exception as e:
                print(f"Erreur produit/quantité : {e}")
                continue

        top = counter.most_common(x)
        return Response([{"product_id": k, "quantity": v} for k, v in top])
