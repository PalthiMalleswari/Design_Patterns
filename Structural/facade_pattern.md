# Design: `BookRide()` Facade — Complete LLD, Code, Diagrams & Interview Prep

**Scope:** Design a `BookRide()` API (like Uber/Ola) that exposes a simple call from the mobile client but internally coordinates: Maps (routing), Pricing, Driver Matching, ETA, Notification, and (optionally) Payment & Booking persistence.

This document contains:
1. Requirements & constraints
2. API definition (public surface)
3. High-level component diagram
4. Class-level design (UML-like ASCII)
5. Sequence diagram (ASCII)
6. Python micro-implementation (clean, testable) — Facade + services
7. Error handling, retries, timeouts, idempotency
8. Scaling, persistence, eventual consistency, async flows
9. Security, observability, monitoring
10. Interview questions + model answers
11. Variations, extensions, and tradeoffs

---

## 1) Requirements & Constraints

**Functional requirements**
- Client calls `POST /bookRide` (or equivalent SDK call) with `user_id`, `source`, `destination`, `ride_options`.
- System returns immediate booking response with `booking_id`, `driver_id`, `estimated_eta`, and fare.
- Internally: compute route, estimate fare, match driver, get ETA, reserve driver, send push/notification.
- Support fallback: if no driver available, return proper status.

**Non-functional**
- Low latency for client (<= 300–800 ms ideally for initial response; matching may continue async).
- Highly available and scalable.
- Idempotent: duplicate client requests (retries) must not create multiple bookings.
- Observable: traces, metrics, logs.

**Assumptions**
- There exist microservices/3rd-party APIs: MapsService, PricingService, DriverMatchingService, ETAService, NotificationService.
- A persistent Booking store (DB) exists for confirmations and later lifecycle events.
- Payment is handled separately (authorization on demand).

---

## 2) Public API (Facade surface)

**REST** (or SDK)
```
POST /bookRide
Request body: {
  user_id: string,
  source: { lat, lng },
  destination: { lat, lng },
  ride_type: string,   # e.g. "regular", "pool", "premium"
  client_request_id: string (for idempotency)
}

200 OK {
  booking_id: string,
  status: "PENDING" | "CONFIRMED" | "REJECTED",
  driver_id: string | null,
  eta_seconds: int | null,
  fare: float | null
}
```

**Key design: `client_request_id`** — used to ensure idempotency across retries.

---

## 3) High-level components

- **RideFacade / BookingFacade** (exposes `book_ride()`)
- **MapsService** (routing, distance)
- **PricingService** (fare calc, surge)
- **DriverMatchingService** (find & reserve driver)
- **ETAService** (ETA calculation; might use driver GPS or predictive model)
- **NotificationService** (push/SMS)
- **BookingRepository** (DB for bookings)
- **EventBus / Message Queue** (Kafka/Rabbit for async steps)

Client -> RideFacade -> calls sync/async services -> BookingRepository & EventBus

---

## 4) UML-like class diagram (ASCII)

```
+-------------------+
|   RideFacade      |
|-------------------|
| +book_ride(req)   |
+-------------------+
        | calls
        v
+-------------------+      +------------------+     +-------------------+
|  MapsService      |      | PricingService   |     | DriverMatchingSvc |
| +get_route()      |      | +estimate_fare() |     | +find_and_reserve()|
+-------------------+      +------------------+     +-------------------+
        |                         |                        |
        v                         v                        v
     (route)                    (fare)                (driver assignment)

+-------------------+    +-------------------+   +-------------------+
| ETAService        |    | NotificationSvc   |   | BookingRepository |
| +estimate_eta()   |    | +notify_user()    |   | +save_booking()   |
+-------------------+    +-------------------+   +-------------------+

EventBus -> async handlers (e.g. confirm driver, cancellation, billing flows)
```

---

## 5) Sequence diagram (simplified ASCII)

```
Client -> RideFacade: book_ride(user, src, dst, req_id)
RideFacade -> BookingRepository: get_or_create_booking(req_id)
alt booking exists
  RideFacade -> Client: return existing booking
else
  RideFacade -> MapsService: route = get_route(src, dst)
  RideFacade -> PricingService: fare = estimate_fare(route, ride_type)
  RideFacade -> DriverMatchingService: driver = find_and_reserve(route, user_pref)
  par
    RideFacade -> ETAService: eta = estimate_eta(driver, route)
    RideFacade -> BookingRepository: save_booking(booking + driver + fare + eta)
    RideFacade -> NotificationService: notify_driver(driver, booking)
  end
  RideFacade -> Client: return booking_id, status, driver, eta, fare
end
```

Notes:
- `get_or_create_booking(req_id)` ensures idempotency.
- `find_and_reserve` must support atomic reserve (or compensation) semantics.

---

## 6) Python micro-implementation

This is a compact, testable example focusing on structure and patterns. It purposely avoids external dependencies.

```python
# services.py - Simple service interfaces and stubs
import uuid
import time
from typing import Optional

class MapsService:
    def get_route(self, src, dst):
        # In real world: call routing engine; return distance (meters), duration (seconds)
        distance_m = 12000
        duration_s = 1800
        return {"distance_m": distance_m, "duration_s": duration_s}

class PricingService:
    def estimate_fare(self, distance_m, duration_s, ride_type):
        base = {"regular": 50, "premium": 120}.get(ride_type, 50)
        per_km = {"regular": 10, "premium": 20}.get(ride_type, 10)
        km = distance_m / 1000.0
        fare = base + per_km * km
        # simple surge example
        surge = 1.0
        return round(fare * surge, 2)

class DriverMatchingService:
    def find_and_reserve(self, src, route, ride_type) -> Optional[dict]:
        # In real: geo-index query + availability check + atomic reservation
        # return None when no driver
        return {"driver_id": "driver-123", "vehicle": "Toyota", "location": src}

class ETAService:
    def estimate_eta(self, driver_location, src):
        # compute ETA from driver->src
        return 300  # seconds

class NotificationService:
    def notify_driver(self, driver_id, message):
        print(f"notify {driver_id}: {message}")

class BookingRepository:
    def __init__(self):
        self.store = {}

    def get_by_request_id(self, client_request_id):
        return self.store.get(client_request_id)

    def save(self, client_request_id, booking):
        self.store[client_request_id] = booking
        return booking


# facade.py
class RideFacade:
    def __init__(self,
                 maps: MapsService,
                 pricing: PricingService,
                 matcher: DriverMatchingService,
                 eta: ETAService,
                 notifier: NotificationService,
                 repo: BookingRepository):
        self.maps = maps
        self.pricing = pricing
        self.matcher = matcher
        self.eta = eta
        self.notifier = notifier
        self.repo = repo

    def book_ride(self, user_id, src, dst, ride_type, client_request_id=None):
        # idempotency key
        if client_request_id is None:
            client_request_id = str(uuid.uuid4())

        existing = self.repo.get_by_request_id(client_request_id)
        if existing:
            print("Returning existing booking")
            return existing

        # 1. Get route
        route = self.maps.get_route(src, dst)

        # 2. Estimate fare
        fare = self.pricing.estimate_fare(route["distance_m"], route["duration_s"], ride_type)

        # 3. Find & reserve driver
        driver = self.matcher.find_and_reserve(src, route, ride_type)
        if not driver:
            booking = {"booking_id": None, "status": "REJECTED", "reason": "NO_DRIVERS"}
            self.repo.save(client_request_id, booking)
            return booking

        # 4. Estimate ETA
        eta_seconds = self.eta.estimate_eta(driver["location"], src)

        # 5. Persist booking
        booking_id = f"bkg-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        booking = {
            "booking_id": booking_id,
            "status": "CONFIRMED",
            "user_id": user_id,
            "driver_id": driver["driver_id"],
            "fare": fare,
            "eta_seconds": eta_seconds,
            "client_request_id": client_request_id,
        }
        self.repo.save(client_request_id, booking)

        # 6. Notify driver async (here sync for example)
        self.notifier.notify_driver(driver["driver_id"], f"New booking {booking_id}")

        return booking


# Quick run example
if __name__ == "__main__":
    facade = RideFacade(MapsService(), PricingService(), DriverMatchingService(), ETAService(), NotificationService(), BookingRepository())
    req_id = "client-req-1001"
    a = facade.book_ride("user1", {"lat": 12.9, "lng": 77.6}, {"lat": 12.98, "lng": 77.7}, "regular", client_request_id=req_id)
    print(a)

```

### Notes on the sample code
- `get_or_create` via `client_request_id` in repository ensures idempotency.
- `find_and_reserve` is modeled as atomic but in real world you'd use distributed locks or transactional reservation.
- Notification is synchronous in this example for simplicity — in real systems it will be async via message queue.

---

## 7) Error handling, retries, and idempotency

**Idempotency**: Provide `client_request_id` (UUID) — BookingRepository uses this to return existing booking.

**Retries**:
- Client retries should be safe: repeat requests with same `client_request_id` return same booking.
- Internal retries: for transient errors (Maps timeout, Pricing failure), apply exponential backoff and circuit breakers.

**Compensation**:
- If driver reserved but DB save fails: either rollback driver reservation or enqueue compensation event on the EventBus to release driver.

**Timeouts**:
- Per-external-call timeouts (e.g. maps: 200 ms; matching: 500 ms)

**Fallbacks**:
- If ETA service fails, return best-effort ETA or `null` and mark booking as `CONFIRMED_WITH_NO_ETA`.

---

## 8) Scaling & async design

**Synchronous vs Asynchronous**
- Keep the client-facing critical path lightweight (route+estimate+quick match). Heavy tasks (detailed pricing, promotions, fraud detection) can be async.
- Use EventBus for post-booking steps: notifications, analytics, invoicing, driver navigation.

**Driver reservation atomicity**
- Use a distributed lock or optimistic compare-and-set on driver record.
- Example flows: claim driver by writing `driver.status=RESERVED` with `version` check.

**Data stores**
- Booking store: main transactional DB (e.g. PostgreSQL) for booking records.
- Driver location store: in-memory store (Redis or specialized geo-index) for fast nearest neighbor queries.

**Scaling patterns**
- Stateless RideFacade instances behind load balancer
- DriverMatching service horizontally scaled with locality partitioning (shard by city/zone)
- Use caching for map tiles/route fragments and pricing parameters

---

## 9) Security & Observability

**Security**
- Authenticate client requests (JWT or signed tokens)
- Authorization: ensure user has the right to book (billing issues)
- Input validation (coordinate ranges)

**Observability**
- Tracing: attach `trace_id` to external calls (Maps, Matching)
- Metrics: booking latency, success rate, no-driver rate, reservation failure rate
- Logs: structured logs with booking_id & client_request_id

---

## 10) Interview questions + model answers

**Q1: Why use a Facade for `book_ride()` instead of letting the client call services directly?**
**A:** The facade hides complexity and cross-service orchestration. It simplifies client code, reduces coupling, enforces business rules and idempotency, centralizes retries/fallbacks, and allows internal services to evolve without affecting clients.

**Q2: How do you ensure idempotency?**
**A:** Use a client-provided `client_request_id` (UUID). Persist booking keyed by this value. If duplicates occur, return the existing booking. Also ensure underlying operations (driver reserve) are implemented with atomic compare-and-set or reservation tokens to avoid double-booking.

**Q3: What happens if driver reservation succeeds but DB write fails?**
**A:** Two approaches: (1) Use distributed transaction patterns (rare at large scale). (2) Use a compensation pattern: enqueue a "release driver" event on failure. Keep retries & monitoring. Prefer to design reservation as idempotent and resilient so repeated attempts lead to consistent state.

**Q4: How to scale driver matching?**
**A:** Partition by geography (city/zone), use geo-index (Redis geo, quadtrees), keep driver location in a fast in-memory store, use async worker pools for heavy matching, and cache common queries. Also apply heuristics to limit search radius.

**Q5: How do you measure and improve latency?**
**A:** Instrumented metrics & traces. Profile each external call (maps, matching). Introduce timeouts & fallbacks. Cache route or fare computations when possible. Keep critical path minimal and offload heavy work to async jobs.

**Q6: How would you handle surge pricing and promotions?**
**A:** Surge and promotions are applied in `PricingService`. Keep pricing rules in a fast-access store (Redis) and update them via config live reload. Validate promotions asynchronously before final billing if they are complex.

**Q7: What about offline drivers / flaky network?**
**A:** Driver presence must be validated at reserve time (last heartbeat), reserve token with TTL, and then require driver ACK. Use retries and escalate if no ACK.

---

## 11) Variations, extensions & tradeoffs

**Make matching async:** Respond to client with `PENDING` and confirm later via push. Tradeoff: faster response vs delayed confirmation.

**Two-phase commit for driver reservation + booking save:** Achieves stronger consistency but is complex and brittle at scale.

**Optimistic UI:** Return a provisional booking to user quickly and confirm once driver accepts — improves UX but increases complexity in cancellations.

**Edge Cases**
- Multiple clients retrying rapidly for the same user — idempotency handles duplicates.
- Driver cancel after reservation — need fallback driver selection and notifications.
- Payment failure after booking — cancel booking and release driver.

---

## Final checklist for interview deliverable

- Explain facade intent: hide complexity and present single API
- Show idempotency mechanism with `client_request_id`
- Show error handling & compensation
- Show scaling (partitioning, caching, async) and monitoring
- Present a clear class/sequence diagram
- Walk through the happy path and 2 failure paths (no driver, DB failure after reserve)

---
