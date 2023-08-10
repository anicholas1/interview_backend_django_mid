
### Intro
Our current project mainly relies on `APIView` in DRF.
This base class comes with the standard HTTP verbs such as GET
and POST, along with a few helper methods such as get_permissions

Here's a tutorial for using APIView:  https://www.django-rest-framework.org/tutorial/3-class-based-views/


Start by creating a class in the app inventory/views.py called 
`InvetoryCreateView` or possibly `InventoryListCreateView` if we
intend on expanding this API further to handle list requests as well.


### Base Class
```python
class InventoryListCreateView(APIView):
    serializer_class = InventorySerializer
```

Key detail here is the APIView from DRF that will give us most of the functionality we need.

Now we can add the create functionality by overriding the post method. Normally,
we don't need to overwrite this if we don't have any custom functionality, but in this case
we need to validate the metadata since it's a JSON field on our Inventory Model.


Below `serializer_class`, define a new method `post`:


### POST method
```python
    def post(self, request: Request, *args, **kwargs) -> Response:
```

Luckily, we already have an InventoryMetaData pydantic class that we can use to validate
the JSON fields. Pydantic is a great library for custom validation and typing.  
Perfect for validating custom json fields, so we aren't dumping random json into our database.
See the docs here: https://docs.pydantic.dev/latest/

We need to add `film_locations` to this model first.
Look in inventory/schema.py to find the model `InventoryMetaData` and add 
`film_locations`: list[tuple].  We can assume it will be a list of tuples for (city, state), but 
we should clarify this with product.

### Create Custom Logic

First, we need to validate the metadata with our custom model since 
it isn't attached to the serializer.

```python
        try:
            metadata = InventoryMetaData(**request.data['metadata'])
        except Exception as e:
            return Response({'error': str(e)}, status=400)
```

This will validate the metadata field in the request body against our pydantic model we just changed.
From here, its quite straightforward, just like any other post view you've made.

```python
        # convert to dict before we pass to serializer
        request.data['metadata'] = metadata.dict()
        
        # use our serializer defined at the top of our class
        serializer = self.serializer_class(data=request.data)
        
        # always validate before returning in the response.  
        # DRF will actually block you if you don't
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
```



### Success!!!

In conclusion, we've done a few things here:

1. Create a new class based view `InventoryListCreateView` using the base `APIView`
2. Added `film_locations` to our pydantic model InventoryMetaData
3. Created a custom `post` method in our new class
4. Validated the metadata from the request body by passing it to our pydantic model
5. Created an Inventory Item by then using serializer.save() like any other view in DRF


