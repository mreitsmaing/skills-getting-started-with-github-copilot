"""Tests for the root endpoint."""

import pytest


class TestRootEndpoint:
    """Test suite for the GET / endpoint."""

    def test_root_returns_redirect(self, client):
        """Test that GET / returns a redirect response."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307

    def test_root_redirects_to_static_index(self, client):
        """Test that GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.headers["location"] == "/static/index.html"

    def test_root_with_follow_redirects(self, client):
        """Test that following the redirect returns the static index page."""
        response = client.get("/", follow_redirects=True)
        # The response should be the HTML file
        assert response.status_code == 200
