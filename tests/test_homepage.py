def test_homepage(client):
    """Test homepage."""
    response = client.get("/")
    assert response.status_code == 200
    assert "No content provided" not in response.data.decode()


def test_empty_post_request_fail(client):
    """Test empty post request."""
    response = client.post("/", follow_redirects=True)
    assert response.status_code == 200
    assert "No content provided" in response.data.decode()


def test_no_social_media_selected_fails(client):
    """Test no social media selected."""
    response = client.post("/", data={"content": "test"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Please select at least 1 social media" in response.data.decode()

