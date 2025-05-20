# my_app/views_lineage.py

import os
import json
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DataVersionView(APIView):
    def get(self, request):
        version_id = request.query_params.get("version")
        if version_id is None:
            return Response({"error": "Parameter 'version' is required."}, status=400)

        try:
            version_id = int(version_id)
        except ValueError:
            return Response({"error": "Version must be an integer."}, status=400)

        dir_path = os.path.join(settings.BASE_DIR, "data_lake", "ALL_TRANSACTIONS_ANONYMIZED", "historique")
        json_files = [f for f in os.listdir(dir_path) if f.endswith(".json")]

        if not json_files:
            return Response({"error": "No data available."}, status=404)

        try:
            json_files.sort(key=lambda f: datetime.strptime(f.split(".json")[0], "%Y-%m-%dT%H-%M-%S.%fZ"))
        except Exception:
            return Response({"error": "Filenames are not in expected timestamp format."}, status=500)

        if version_id < 1 or version_id > len(json_files):
            return Response({"error": "Version not found."}, status=404)

        version_file = json_files[version_id - 1]
        full_path = os.path.join(dir_path, version_file)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = json.load(f)
        except Exception as e:
            return Response({"error": f"Failed to load version: {str(e)}"}, status=500)

        return Response({
            "version_id": version_id,
            "filename": version_file,
            "data": content
        })
