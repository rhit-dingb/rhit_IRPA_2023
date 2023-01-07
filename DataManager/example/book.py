class Book():
    def __init__(self,id, title, authors, isbn, numberOfPages, borrower, isAvailable):
        self.id = id
        self.title = title
        self.authors = authors
        self.isbn = isbn
        self.numberOfPages = numberOfPages
        self.borrower = borrower
        self.isAvailable = isAvailable
    
    def __repr__(self):
        return self.__dict__