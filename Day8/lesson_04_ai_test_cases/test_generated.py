from main import app

import pytest
from fastapi.testclient import TestClient


# ID는 계약 기반 테스트 표의 행과 연결됩니다.
# 기대값은 현재 구현을 호출해서 계산하지 않고 업무 계약에서 정했습니다.
@pytest.mark.parametrize("amount, discount, payable", [
    pytest.param(5000, 0, 5000, id="N01"),
    pytest.param(20000, 1000, 19000, id="N02"),
    pytest.param(1, 0, 1, id="E01"),
    pytest.param(100000, 1000, 99000, id="E02"),
    pytest.param(9999, 0, 9999, id="R01"),
    pytest.param(10000, 1000, 9000, id="R02"),
    pytest.param(10001, 1000, 9001, id="R03"),
])
def test_quote_success(amount, discount, payable):
    with TestClient(app) as client:
        response = client.post("/quotes", json={"amount": amount})
    assert response.status_code == 200
    assert response.json() == {
        "amount": amount, "discount": discount, "payable": payable,
    }


@pytest.mark.parametrize("body", [
    pytest.param({"amount": 0}, id="B01"),
    pytest.param({"amount": 100001}, id="B02"),
    pytest.param({}, id="M01"),
    pytest.param({"amount": "10000"}, id="T01"),
    pytest.param({"amount": 10000.0}, id="T02"),
    pytest.param({"amount": 1.5}, id="T03"),
    pytest.param({"amount": True}, id="T04"),
    pytest.param({"amount": None}, id="T05"),
    pytest.param({"amount": []}, id="T06"),
    pytest.param({"amount": {}}, id="T07"),
])
def test_quote_invalid(body):
    with TestClient(app) as client:
        response = client.post("/quotes", json=body)
    # 오류 본문 형식은 계약에 없으므로 상태 코드만 검사합니다.
    assert response.status_code == 422


def test_quote_missing_body_M02():
    with TestClient(app) as client:
        response = client.post("/quotes")
    assert response.status_code == 422
