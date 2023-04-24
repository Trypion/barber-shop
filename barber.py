import threading
import time

n = 20
customers = 0
mutex = threading.Semaphore(1)
sofa = threading.Semaphore(4)
customer1 = threading.Semaphore(0)
customer2 = threading.Semaphore(0)
barber = threading.Semaphore(0)
payment = threading.Semaphore(0)
receipt = threading.Semaphore(0)
queue1 = []
queue2 = []


def customer():
    global customers
    sem1 = threading.Semaphore(0)
    sem2 = threading.Semaphore(0)
    mutex.acquire()
    if customers == n:
        mutex.release()
        balk()
        return
    customers += 1
    queue1.append(sem1)
    mutex.release()

    # enterShop()
    print("Customer entered the shop.")
    customer1.release()
    sem1.acquire()

    sofa.acquire()
    # sitOnSofa()
    print("Customer sat on the sofa.")
    sem1.release()
    mutex.acquire()
    queue2.append(sem2)
    mutex.release()
    customer2.release()
    sem2.acquire()
    sofa.release()

    # sitInBarberChair()
    print("Customer sat in the barber chair.")

    # pay()
    print("Customer paid.")
    payment.release()
    receipt.acquire()
    mutex.acquire()
    customers -= 1
    mutex.release()


def barber():
    while True:
        customer1.acquire()
        mutex.acquire()
        sem = queue1.pop(0)
        sem.release()
        sem.acquire()
        mutex.release()
        sem.release()
        customer2.acquire()
        mutex.acquire()
        sem = queue2.pop(0)
        mutex.release()
        sem.release()
        # barber.release()
        cutHair()
        # print("Barber cut the customer's hair.")
        payment.acquire()
        # acceptPayment()
        print("Barber accepted the payment.")
        receipt.release()


def balk():
    print("Balk: Customer left because the shop is full.")


def cutHair():
    print("Barber is cutting the customer's hair.")
    time.sleep(5)
    print("Barber finished cutting the customer's hair.")


# Create barber thread
barber_thread = threading.Thread(target=barber)
barber_thread.start()

# Create customer threads
customer_threads = []
for i in range(n):
    customer_thread = threading.Thread(target=customer)
    customer_threads.append(customer_thread)
    customer_thread.start()

# Wait for all customer threads to finish
for customer_thread in customer_threads:
    customer_thread.join()



barber_thread.join()
