
from faker import Faker
import csv
import uuid
from datetime import timedelta, datetime
import random

fake = Faker("fr_FR")

products = ["ASSURANCE_A",
            "ASSURANCE_B",
            "CARTE_CREDIT",
            "LEASING_VOITURE",
            "LOCATION"]

document_types= ["CNI", "PAYSLIP", "RIB", "TAX_NOTICE"]


documents = dict((p, random.sample(document_types, 2 + random.randrange(2))) for p in products) 

nb_files = 5000

def random_date(start, delta):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def main():
    
    with open('client_files.csv', 'w') as client_csvfile, open("events.csv", 'w') as events_csvfile :
        fieldnames_client = ['uuid','date_created','product','first_name', 'last_name','dob']
        clients = csv.DictWriter(client_csvfile, delimiter=';',fieldnames=fieldnames_client)
        clients.writeheader()
        fieldnames_events = ['timestamp', 'client_uuid', 'type', 'doc_type', 'status']
        events = csv.DictWriter(events_csvfile,  delimiter=';',fieldnames=fieldnames_events)
        events.writeheader()
        
        start = datetime(2017,1,1)
        for i in range(nb_files):
            client_uuid = uuid.uuid4()
            freq = (start.hour - 16) ** 2 + 2
            creation_date = random_date(start, timedelta(minutes=freq))
            product = products[random.randrange(len(products))]
            start = creation_date
            clients.writerow({"uuid":str(client_uuid),
                              "date_created":start.isoformat(),
                              "product": product,
                              "first_name":fake.first_name_male(),
                              "last_name":fake.last_name(),
                              "dob":fake.past_date() - timedelta(days=20*365)})
            
            event_time = creation_date
            for doc in documents[product] :
                for i in range(3):
                    ok = random.random() > 0.4
                    event_time = random_date(event_time, timedelta(minutes=5))
                    type_ = "DOC"
                    events.writerow({"timestamp": event_time,
                                     "client_uuid": client_uuid,
                                     "type": type_,
                                     "doc_type":doc,
                                     "status":ok})
                    if ok :
                        break
            if random.random() < 0.95 :
                event_time = random_date(event_time, timedelta(minutes=10))
                type_ = "SIG"
                events.writerow({"timestamp": event_time,
                                 "client_uuid": client_uuid,
                                 "type": "SIGNATURE",
                                 "status": True})

if __name__ == "__main__":
    main()
