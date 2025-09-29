import csv

data = [
    ["FirstName__c", "LastName__c", "Company__c", "Email__c", "Lead_Status__c"],
    ["Aarav", "Sharma", "Innovate Inc.", "a.sharma@innovate.com", "New"],
    ["Fatima", "Al-Fassi", "Tech Solutions", "fatima.f@techsol.com", "New"],
    ["Kai", "Johnson", "Quantum Computing", "kai.j@quantum.com", "New"],
    ["Chloe", "Nguyen", "Digital Dynamics", "chloe.n@digidyn.com", "New"],
    ["Liam", "Smith", "Global Connect", "l.smith@globalconnect.com", "New"]
]

with open('leads.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
