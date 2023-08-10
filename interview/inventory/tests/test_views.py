from datetime import datetime, timedelta
import pytz

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from interview.inventory.models import Inventory


class TestInventoryViews(APITestCase):

    def setUp(self):
        # create several good and bad dates to make sure incorrect
        # inventory doesn't leak through!
        self.url = reverse('inventory-list-by-date')
        self.item_1 = Inventory.objects.create(metadata={"incorrect": True})
        self.created_at = datetime.now(pytz.utc) - timedelta(20)
        self.item_1.created_at = self.created_at
        self.item_1.save()
        self.item_2 = Inventory.objects.create(metadata={"correct": True})
        self.item_2.created_at = self.item_2.created_at.replace(tzinfo=pytz.utc)
        self.item_2.save()

    def test_get_inventory_by_created_date(self):
        created_at = datetime.now(pytz.utc) - timedelta(5)
        query_params = {"created_at": created_at}
        response = self.client.get(self.url, query_params)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        data = response.data[0]
        assert data["metadata"] == {"correct": True}

        # Add more checks on all fields to make sure everything is correct.
        # Don't want any false positives!
        # for item in response.data:
        #     print(self.item_2.created_at)
        #     print(item["created_at"])
        #     assert item["created_at"] == self.item_2.created_at

    def test_no_inventory_returned(self):
        created_at = datetime.now(pytz.utc) + timedelta(1)
        query_params = {"created_at": created_at}
        response = self.client.get(self.url, query_params)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0



