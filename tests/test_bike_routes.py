def test_empty_get_all_bikes_returns_empty_list(client):
    response = client.get("/bike") #runs the get request
    response_body = response.get_json() #puts response in a JSON format
    
    assert response.status_code == 200 #attrb that lets us get the status code from response
    assert response_body == []
    
def test_get_one_bike_with_empty_db_returns_404(client):
    response = client.get("/bike/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert "message" in response_body #how is "message" doing anything????
    
def test_get_one_bike_with_populated_db_returns_bike_json(client, add_two_bikes):
    response = client.get("/bike/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"id":1, "name":"Speedy", "price":1, "size":6, "type":"racing"}

def test_post_one_bike_creates_bike_in_populated_db(client, add_two_bikes): #new bike being posted should have id of 3 since we're putting in add_two_bikes - personal choice
    response = client.post("/bike", json={"name":"Shiny new bike", "size":10, "price":3, "type":"birthday gift"}) #second item being passed in should be requeset body #order for response body keys doesn't matter
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["id"] == 3
    assert "id" in response_body

def test_post_one_bike_creates_one_bike_in_db(client):
    response = client.post("/bike", json={"name":"Shiny new bike", "size":10, "price":3, "type":"birthday gift"}) #second item being passed in should be requeset body #order for response body keys doesn't matter
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["id"] == 1
    assert "id" in response_body

def test_get_all_bikes_returns_2_bikes(client, add_two_bikes):
    response = client.get("/bike")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [{"id": 1, "name":"Speedy", "price":1, "size":6, "type":"racing"}, 
    {"id": 2, "name":"Motorbike", "price":6, "size":2, "type":"Motor"}]
    assert len(response_body) == 2

