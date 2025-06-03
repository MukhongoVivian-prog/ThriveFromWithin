from rest_framework import viewsets, permissions
from .models import Benefit, BenefitCategory
from .serializers import BenefitSerializer, BenefitCategorySerializer

class BenefitCategoryViewSet(viewsets.ModelViewSet):
    queryset = BenefitCategory.objects.all()
    serializer_class = BenefitCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all().order_by('-created_at')
    serializer_class = BenefitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
