from sqlmodel import select

from housenomics.transaction import Transaction


class ServiceListTransactions:
    def execute(self, session):
        statement = select(Transaction)
        results = session.exec(statement)
        return results
