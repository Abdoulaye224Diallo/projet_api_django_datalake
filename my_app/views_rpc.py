# my_app/views_rpc.py
from rest_framework.views import APIView
from rest_framework.response import Response
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification


class TriggerMLTrainingView(APIView):
    def post(self, request):
        try:
            # Dummy data
            X, y = make_classification(n_samples=100, n_features=5, random_state=42)
            model = LogisticRegression()
            model.fit(X, y)
            score = model.score(X, y)

            return Response({
                "message": "Model trained successfully.",
                "accuracy": score
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
