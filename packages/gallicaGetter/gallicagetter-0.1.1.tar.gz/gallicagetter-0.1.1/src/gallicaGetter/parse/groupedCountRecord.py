class GroupedCountRecord:

    def __init__(self, date, count, ticketID, term, requestID):
        self.date = date
        self.count = count
        self.term = term
        self.ticketID = ticketID
        self.requestID = requestID

    def getRow(self):
        row = [
            self.date.getYear(),
            self.date.getMonth(),
            self.date.getDay(),
            self.term
        ]
        (self.ticketID is not None) and row.append(self.ticketID)
        (self.requestID is not None) and row.append(self.requestID)
        row.append(self.count)
        return tuple(row)

    def getDisplayRow(self):
        return (
            self.term,
            self.date.getYear(),
            self.date.getMonth(),
            self.date.getDay(),
            self.count
        )

    def __repr__(self):
        return f'GroupedCountRecord({self.date}, {self.term}, {self.count})'


