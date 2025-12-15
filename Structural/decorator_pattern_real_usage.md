# Resilient Systems with Retry and Circuit Breaker

---

## 1. What is Resilience?

**Resilience** is the ability of a system to **continue functioning reasonably well even when some of its dependencies fail**.

In modern distributed systems (microservices, cloud, third‑party APIs), failures are **normal**, not exceptional.

A resilient system:

* Expects failures
* Limits the impact of failures
* Recovers automatically

---

## 2. Why Resilience is Needed

In real systems:

* Networks are unreliable
* External APIs go down
* Services become slow

Without resilience, a single failing dependency can cause **cascading failures**, taking down the entire application.

---

## 3. Retry Pattern

### What is Retry?

**Retry** means:

> If a request fails due to a *temporary* issue, try again after a short delay.

### When Retry Helps

* Network glitches
* Temporary timeouts
* Random 5xx errors

### When Retry Hurts

* Service is completely DOWN
* Unlimited retries increase load

Retry must be **limited and controlled**.

---

## 4. Circuit Breaker Pattern

### What is a Circuit Breaker?

A **Circuit Breaker** protects the system by **stopping calls to a failing dependency**.

Think of it like an electrical fuse.

### Circuit Breaker States

| State     | Meaning            |
| --------- | ------------------ |
| CLOSED    | Normal operation   |
| OPEN      | Calls blocked      |
| HALF-OPEN | Test calls allowed |

---

## 5. Retry vs Circuit Breaker

| Aspect  | Retry                    | Circuit Breaker  |
| ------- | ------------------------ | ---------------- |
| Purpose | Handle temporary failure | Prevent overload |
| Action  | Re-attempt request       | Block requests   |
| Risk    | Can overload system      | Protects system  |

They are **complementary**, not alternatives.

---

## 6. User Request Flow Diagrams

### 6.1 Without Resilience (Problem)

```
User
 ↓
Service A
 ↓
Service B ❌ (DOWN)
 ↓
Threads waiting
 ↓
Threads exhausted
 ↓
Service A crashes
```

---

### 6.2 With Retry Only

```
User
 ↓
Service A
 ↓
Retry #1 → Service B ❌
 ↓
Retry #2 → Service B ❌
 ↓
Retry #3 → Service B ❌
 ↓
Failure
```

Retry helps only for **short outages**.

---

### 6.3 With Circuit Breaker Only

```
User Request 1 → Service B ❌
User Request 2 → Service B ❌
User Request 3 → Circuit OPEN 🚨

Further requests blocked immediately
```

System remains healthy.

---

### 6.4 With Retry + Circuit Breaker (Ideal)

```
User
 ↓
Circuit Breaker (CLOSED)
 ↓
Retry Logic
 ↓
Service B
```

* Retry handles temporary failures
* Circuit breaker prevents cascading failures

---

## 7. Correct Order of Execution

✅ Correct:

```
Circuit Breaker
  → Retry
     → Service B
```

❌ Wrong:

```
Retry
  → Circuit Breaker
```

---

## 8. Code Example (Python)

### 8.1 Service B (Downstream Service)

```python
import random

class ServiceB:
    def call(self):
        print("Service B called")
        if random.choice([True, False]):
            raise Exception("Service B failed")
        return "Success from Service B"
```

---

### 8.2 Retry Decorator

```python
import time

class Retry:
    def __init__(self, service, retries=3, delay=1):
        self.service = service
        self.retries = retries
        self.delay = delay

    def call(self):
        last_exception = None
        for attempt in range(1, self.retries + 1):
            try:
                print(f"Retry attempt {attempt}")
                return self.service.call()
            except Exception as e:
                last_exception = e
                time.sleep(self.delay)
        raise last_exception
```

---

### 8.3 Circuit Breaker Decorator

```python
import time

class CircuitBreaker:
    def __init__(self, service, failure_threshold=2, recovery_time=5):
        self.service = service
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def call(self):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_time:
                self.state = "HALF-OPEN"
                print("Circuit HALF-OPEN")
            else:
                raise Exception("Circuit is OPEN")

        try:
            result = self.service.call()
            self.failure_count = 0
            self.state = "CLOSED"
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print("Circuit OPENED")
            raise e
```

---

### 8.4 Service A (Caller Service)

```python
class ServiceA:
    def __init__(self, service_b):
        self.service_b = service_b

    def process_request(self):
        return self.service_b.call()
```

---

### 8.5 Wiring Everything Together

```python
service_b = ServiceB()
service_b = Retry(service_b, retries=3, delay=1)
service_b = CircuitBreaker(service_b, failure_threshold=2, recovery_time=10)

service_a = ServiceA(service_b)

try:
    print(service_a.process_request())
except Exception as e:
    print("Request failed:", e)
```

---

## 9. Key Takeaways

* Failures are normal in distributed systems
* Retry handles **temporary** failures
* Circuit breaker prevents **system overload**
* Together they provide **resilience**
* Decorator pattern allows clean composition

---

## 10. Interview One-Liner

> Resilience is the ability of a system to handle failures gracefully. Retry addresses transient failures, while circuit breakers prevent cascading failures by stopping calls to unhealthy services.

---

## 11. Retry vs Idempotency (Common Interview Trap)

### 11.1 What is Idempotency?

**Idempotency** means:

> Performing the same operation multiple times produces the **same final result** as performing it once.

In simple words:

* First request → does the work
* Repeated requests → do **not** change the outcome

---

### 11.2 Real-Life Analogy

**Elevator Button** 🚪

* You press the button once → elevator is called
* You press it 10 times → still only one elevator arrives

The action is **idempotent**.

---

### 11.3 Retry vs Idempotency (Conceptual Difference)

| Aspect     | Retry                     | Idempotency                    |
| ---------- | ------------------------- | ------------------------------ |
| What it is | Client-side behavior      | Operation property             |
| Purpose    | Handle transient failures | Prevent duplicate effects      |
| Risk       | Duplicate execution       | Safe repeated execution        |
| Scope      | How many times you call   | What happens when called again |

---

### 11.4 Why This Becomes Dangerous in Real Systems

Consider a **Payment API**:

```
POST /pay
```

* Request sent
* Payment succeeds
* Network times out before response

Client thinks:

> "Payment failed, retry"

Result:

* 💸 **Money debited twice**

This happens when **retry is used without idempotency**.

---

### 11.5 Which HTTP Methods Are Idempotent?

| Method | Idempotent | Reason               |
| ------ | ---------- | -------------------- |
| GET    | ✅          | Read-only            |
| PUT    | ✅          | Replaces resource    |
| DELETE | ✅          | Deletes once         |
| POST   | ❌          | Creates new resource |

---

### 11.6 Making Non-Idempotent APIs Safe (Idempotency Key)

**Solution:** Use an **Idempotency Key**

* Client generates a unique key
* Server stores the key + result
* Repeated requests with same key return same result

---

### 11.7 Idempotent Payment Example

#### Client Request

```http
POST /pay
Idempotency-Key: abc-123
```

---

#### Server Logic

```python
class PaymentService:
    def __init__(self):
        self.processed_requests = {}

    def pay(self, idempotency_key, amount):
        if idempotency_key in self.processed_requests:
            return self.processed_requests[idempotency_key]

        # Perform payment once
        result = f"Paid {amount}" 
        self.processed_requests[idempotency_key] = result
        return result
```

---

### 11.8 Retry + Idempotency + Circuit Breaker (Correct Setup)

```
Client
 ↓
Retry Logic
 ↓
Circuit Breaker
 ↓
Idempotent API
```

* Retry handles temporary failures
* Circuit breaker protects system
* Idempotency prevents duplicate side effects

---

### 11.9 Interview Red-Flag Statement (Avoid This ❌)

> "We retry payment APIs to ensure success"

❌ This is dangerous without idempotency.

---

### 11.10 Interview-Ready Golden Answer ✅

> Retry handles transient failures, but retries must be combined with idempotency to prevent duplicate side effects. Circuit breakers protect the system when failures persist. Together, they form a safe and resilient design.
