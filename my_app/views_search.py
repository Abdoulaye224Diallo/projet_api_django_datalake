import os
import json
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


class FullTextSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q")
        start_date_str = request.query_params.get("start_date")

        if not query or not start_date_str:
            return Response({"error": "You must provide 'q' and 'start_date' parameters."}, status=400)

        try:
            start_date = datetime.fromisoformat(start_date_str)
        except:
            return Response({"error": "Invalid start_date format. Use ISO format (e.g., 2023-05-01T00:00:00)"}, status=400)

        data_lake_dir = os.path.join(settings.BASE_DIR, 'data_lake')
        found_items = []
        found_files = set()

        for root, _, files in os.walk(data_lake_dir):
            for file in files:
                if not file.endswith(".json"):
                    continue
                file_path = os.path.join(root, file)
                try:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mtime < start_date:
                        continue

                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        if isinstance(content, dict):
                            content = [content]
                        for obj in content:
                            if query in json.dumps(obj):
                                found_items.append(obj)
                                found_files.add(file_path)
                except Exception as e:
                    continue

        return Response({
            "results_count": len(found_items),
            "resources": list(found_files),
            "matches": found_items
        })
