from sqlmodel import select

from housenomics.transaction import Transaction


class ServiceDetermineSellerTotal:
    def execute(self, lookup, session):
        statement = select(Transaction)
        results = session.exec(statement)
        clean_movements = []
        for m in results:
            clean_movements.append(
                {
                    "description": m.description,
                    "value": m.value,
                }
            )
        total: float = 0
        for movement in clean_movements:
            if lookup.lower() in str(movement["description"]).lower():
                total += float(movement["value"])  # type: ignore
        return total
