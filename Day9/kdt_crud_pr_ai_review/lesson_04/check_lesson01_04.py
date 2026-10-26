from fastapi.testclient import TestClient

import lesson01_04 as api


def check():
    # 매번 동일한 초기 상태에서 테스트합니다.
    api.tasks[:] = [{"id": 1, "name": "홍길동", "message": "동해번쩍"}]
    api.next_id = 2

    with TestClient(api.app) as client:
        result = client.get("/tasks/1")
        assert result.status_code == 200
        assert result.json() == api.tasks[0]
        assert client.get("/tasks/999").status_code == 404
        for invalid_id in (0, -1, "abc"):
            assert client.get(f"/tasks/{invalid_id}").status_code == 422
        print("GET: 조회 200, 없는 id 404, 잘못된 id 422")

        result = client.post("/tasks", json={"name": "김철수", "message": "안녕"})
        assert result.status_code == 201
        assert result.json() == {"id": 2, "name": "김철수", "message": "안녕"}
        assert len(client.get("/tasks").json()) == 2
        for body in ({"name": "", "message": "안녕"}, {"name": "김철수"}):
            assert client.post("/tasks", json=body).status_code == 422
        print("POST: 생성 201, 빈 문자열/필수값 누락 422")

        result = client.put("/tasks/2", json={"name": "이영희", "message": "전체 교체"})
        assert result.status_code == 200
        assert result.json() == {"id": 2, "name": "이영희", "message": "전체 교체"}
        assert client.put("/tasks/2", json={"name": "누락"}).status_code == 422
        assert client.get("/tasks/2").json() == result.json()
        print("PUT: 전체 교체 200, message 누락 422")

        result = client.patch("/tasks/2", json={"name": "박민수"})
        assert result.status_code == 200
        assert result.json() == {"id": 2, "name": "박민수", "message": "전체 교체"}
        result = client.patch("/tasks/2", json={"message": "부분 수정"})
        assert result.status_code == 200
        assert result.json() == {"id": 2, "name": "박민수", "message": "부분 수정"}
        assert client.patch("/tasks/2", json={}).json() == result.json()
        for field in ("name", "message"):
            for invalid_value in ("", None):
                assert client.patch("/tasks/2", json={field: invalid_value}).status_code == 422
        assert client.get("/tasks/2").json() == result.json()
        print("PATCH: 부분 수정 200, 생략한 값 유지, 빈 문자열/null 422")

        for method in (client.put, client.patch):
            assert method("/tasks/999", json={"name": "없음", "message": "없음"}).status_code == 404

        result = client.delete("/tasks/2")
        assert result.status_code == 204 and result.content == b""
        assert client.get("/tasks/2").status_code == 404
        assert client.delete("/tasks/2").status_code == 404
        print("DELETE: 삭제 204, 삭제한 데이터 조회/재삭제 404")

        # 전부 삭제해도 생성할 수 있고, 삭제된 id를 재사용하지 않습니다.
        assert client.delete("/tasks/1").status_code == 204
        assert client.get("/tasks").json() == []
        result = client.post("/tasks", json={"name": "새 사용자", "message": "재생성"})
        assert result.status_code == 201 and result.json()["id"] == 3

    print("PASS: 모든 테스트 통과")


if __name__ == "__main__":
    check()
