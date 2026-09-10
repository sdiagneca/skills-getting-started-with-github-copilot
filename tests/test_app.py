from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    # (no setup needed)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    # Arrange
    # (no setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    chess_club = body["Chess Club"]
    assert set(["description", "schedule", "max_participants", "participants"]).issubset(chess_club.keys())


def test_signup_for_activity_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Nonexistent Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_twice_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"  # already signed up for Chess Club

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"  # already signed up for Chess Club

    # Act
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_from_nonexistent_activity_returns_404(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Nonexistent Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_unregistered_student_returns_404(client):
    # Arrange
    email = "notsignedup@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
