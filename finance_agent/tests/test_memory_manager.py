from app.memory.long_term import JsonLongTermMemory
from app.memory.memory_manager import MemoryManager
from app.memory.short_term import ShortTermMemory


class TestShortTermMemory:
    def test_add_and_get(self):
        mem = ShortTermMemory()
        mem.add_message("user", "hello")
        mem.add_message("assistant", "hi there")
        history = mem.get_history()
        assert len(history) == 2
        assert history[0] == {"role": "user", "content": "hello"}

    def test_clear(self):
        mem = ShortTermMemory()
        mem.add_message("user", "hello")
        mem.clear()
        assert mem.get_history() == []

    def test_max_buffer(self):
        mem = ShortTermMemory()
        for i in range(25):
            mem.add_message("user", f"msg {i}")
        assert len(mem.get_history()) == 20
        assert mem.get_history()[0]["content"] == "msg 5"


class TestLongTermMemory:
    def test_store_and_retrieve(self, tmp_path):
        path = str(tmp_path / "memory.json")
        mem = JsonLongTermMemory(path=path)
        mem.store("budget_goal", "spend less than $500 on food")
        results = mem.retrieve("budget")
        assert len(results) == 1
        assert "500" in results[0]

    def test_retrieve_no_match(self, tmp_path):
        path = str(tmp_path / "memory.json")
        mem = JsonLongTermMemory(path=path)
        mem.store("budget_goal", "spend less on food")
        results = mem.retrieve("xyz_nomatch")
        assert results == []

    def test_clear(self, tmp_path):
        path = str(tmp_path / "memory.json")
        mem = JsonLongTermMemory(path=path)
        mem.store("key", "value")
        mem.clear()
        assert mem.retrieve("key") == []


class TestMemoryManager:
    def test_coordinates_both(self, tmp_path):
        short = ShortTermMemory()
        long = JsonLongTermMemory(path=str(tmp_path / "mem.json"))
        mgr = MemoryManager(short_term=short, long_term=long)

        mgr.add_conversation("user", "hello")
        mgr.store_fact("budget", "limit $1000/month")

        ctx = mgr.get_context("budget")
        assert len(ctx["conversation"]) == 1
        assert len(ctx["facts"]) == 1

    def test_clear_all(self, tmp_path):
        short = ShortTermMemory()
        long = JsonLongTermMemory(path=str(tmp_path / "mem.json"))
        mgr = MemoryManager(short_term=short, long_term=long)

        mgr.add_conversation("user", "hi")
        mgr.store_fact("key", "val")
        mgr.clear_all()

        ctx = mgr.get_context("key")
        assert ctx["conversation"] == []
        assert ctx["facts"] == []
