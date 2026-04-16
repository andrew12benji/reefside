"""Tests for Aqua Quest leaderboard API"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')


def test_api_root():
    r = requests.get(f"{BASE_URL}/api/")
    assert r.status_code == 200
    assert 'message' in r.json()


def test_post_leaderboard_story():
    payload = {"name": "TEST01", "score": 5000, "level": 1, "mode": "story"}
    r = requests.post(f"{BASE_URL}/api/leaderboard", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data['name'] == 'TEST01'
    assert data['score'] == 5000
    assert data['mode'] == 'story'
    assert 'id' in data


def test_post_leaderboard_arcade():
    payload = {"name": "arcplr", "score": 9999, "level": 5, "mode": "arcade"}
    r = requests.post(f"{BASE_URL}/api/leaderboard", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data['name'] == 'ARCPLR'
    assert data['mode'] == 'arcade'


def test_post_leaderboard_name_sanitized():
    """Name should be uppercased and truncated to 6 chars"""
    payload = {"name": "toolongname", "score": 100, "level": 1, "mode": "story"}
    r = requests.post(f"{BASE_URL}/api/leaderboard", json=payload)
    assert r.status_code == 200
    assert len(r.json()['name']) <= 6
    assert r.json()['name'] == r.json()['name'].upper()


def test_get_leaderboard():
    r = requests.get(f"{BASE_URL}/api/leaderboard")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    # should be sorted by score desc
    if len(data) >= 2:
        assert data[0]['score'] >= data[1]['score']


def test_get_leaderboard_filter_mode():
    r = requests.get(f"{BASE_URL}/api/leaderboard?mode=arcade")
    assert r.status_code == 200
    data = r.json()
    for entry in data:
        assert entry['mode'] == 'arcade'


def test_get_leaderboard_limit():
    r = requests.get(f"{BASE_URL}/api/leaderboard?limit=3")
    assert r.status_code == 200
    assert len(r.json()) <= 3
