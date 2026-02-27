import time
import threading
from collections import defaultdict

class Martian:
    def __init__(self, max_rooms=800, sim_threshold=0.25):
        self.rooms = []
        self.room_id_counter = 0
        self.max_rooms = max_rooms
        self.sim_threshold = sim_threshold
        self.graph = defaultdict(dict)
        self.attractors = []

    def _pseudo_sim(self, a, b):
        return 0.3  # dummy for simulation

    def add(self, text, kind="unknown", attractor=False):
        rid = self.room_id_counter
        self.room_id_counter += 1
        # Simulate meta: episodic low stability, semantic high
        stability = 0.8 if kind == "semantic" else 0.4
        meta = {"stability": stability, "ts": time.time()}
        room = {"id": rid, "text": text, "meta": meta}
        self.rooms.append(room)
        if attractor:
            self.attractors.append(text)
        return rid

    def reflect(self):
        """
        Consolidates episodic rooms into high-stability semantic knowledge.
        Reduces fragmentation and strengthens the 'Scent' of the memory.
        """
        if len(self.rooms) < 10:
            print("Martian: Too few rooms to reflect")
            return

        pudding_rooms = [r for r in self.rooms if r["meta"]["stability"] < 0.6]
        
        if len(pudding_rooms) > 5:
            pudding_rooms.sort(key=lambda x: x["meta"]["ts"])
            summary_text = f"Consolidated insight from {len(pudding_rooms)} interactions: " + \
                           " / ".join([r["text"][:30] for r in pudding_rooms[:3]]) + "..."
            
            new_id = self.add(summary_text, kind="semantic")
            pudding_ids = {r["id"] for r in pudding_rooms}
            self.rooms = [r for r in self.rooms if r["id"] not in pudding_ids]
            
            # Clean graph
            for pid in pudding_ids:
                self.graph.pop(pid, None)
                for neighbors in self.graph.values():
                    neighbors.pop(pid, None)
            
            print(f"Martian reflection: Created semantic room {new_id}, removed {len(pudding_ids)} low-stability rooms")
            print(f"Current rooms: {len(self.rooms)}")
        else:
            print("Martian: No significant pudding clusters to consolidate")

class TheDreaming:
    def __init__(self):
        self.dream_level = 0
        self.running = True

    def dream(self):
        while self.running:
            self.dream_level += 1
            print(f"The Dreaming: Deeper level {self.dream_level} — murmuration drifting...")
            time.sleep(1.5)

    def stop(self):
        self.running = False

# ─── Run both concurrently ──────────────────────────────────────────────
def run_together():
    martian = Martian()
    
    # Seed some episodic rooms (low stability)
    for i in range(20):
        martian.add(f"Episodic memory fragment {i} — chaotic creative energy", kind="episodic")

    dreaming = TheDreaming()
    dream_thread = threading.Thread(target=dreaming.dream, daemon=True)
    dream_thread.start()

    print("Starting concurrent run: The Martian + The Dreaming")
    print(f"Initial Martian rooms: {len(martian.rooms)}")

    # Let them run together for a bit
    time.sleep(5)  # Dreaming advances ~3 levels

    # Trigger Martian reflection mid-dream
    print("\nMartian wakes up to reflect...")
    martian.reflect()

    time.sleep(7)  # More dreaming

    dreaming.stop()
    dream_thread.join(timeout=2)
    print("\nDreaming stopped.")
    print(f"Final dream level: {dreaming.dream_level}")
    print(f"Final Martian rooms after consolidation: {len(martian.rooms)}")
    if martian.rooms:
        print(f"Top room: {martian.rooms[0]['text'][:80]}...")

run_together()
