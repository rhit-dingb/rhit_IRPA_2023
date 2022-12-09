from book import Book
from borrower import Borrower
from dbCommunicator import DbCommunicator
from bson.dbref import DBRef
from pymongo import MongoClient

BOOK_TITLE_KEY = "TITLE"
AUTHORS_KEY = "Authors"
ISBN_KEY = "ISBN"
NUMBER_OF_PAGES_KEY = "NumberOfPages"
BORROWER_KEY = "Borrower"
IS_AVAILABLE_KEY = "IsAvailable"

BORROWER_NAME_KEY = "Name"
BORROWER_USERNAME_KEY = "Username"
BORROWER_PHONE = "Phone"

BOOKS_COLLECTION_KEY = "books"
BORROWER_COLLECTION_KEY = "borrowers"

class Library():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['library']

    def addBook(self,book):
        
        if book.title == None or book.authors == None or book.isbn is None or book.numberOfPages is None: 
            return
        
        bookData = ({
            BOOK_TITLE_KEY: book.title,
            ISBN_KEY: book.isbn,
            NUMBER_OF_PAGES_KEY: book.numberOfPages,
            AUTHORS_KEY: book.authors,
            BORROWER_KEY: None,
            IS_AVAILABLE_KEY: True
        })
        
        result = self.db[BOOKS_COLLECTION_KEY].insert_one(bookData)
        book.id = result.inserted_id
        
    
    def addBorrower(self, borrower):
        borrowerData = ({
            BORROWER_NAME_KEY: borrower.name,
            BORROWER_USERNAME_KEY: borrower.username,
            BORROWER_PHONE: borrower.phone
        })
        
        
        result = self.db[BORROWER_COLLECTION_KEY].insert_one(borrowerData)
        borrower.id = result.inserted_id
        
    def checkOutBook(self, borrower, book):
        book.isAvailable = False
        book.borrower = borrower.id
        self.updateBooksInfo(book)
        
    def returnBook(self, borrower, book):
        book.isAvailable = True
        book.borrower = None
        self.updateBooksInfo(book)
    
    def deleteBook(self,id):
        self.db.books.delete_one({
            "_id": id
        })
        
    def updateBooksInfo(self, updatedBook : Book):
        
        updatedData = {
            BOOK_TITLE_KEY: updatedBook.title, 
            ISBN_KEY: updatedBook.isbn, 
            AUTHORS_KEY: updatedBook.authors,
            NUMBER_OF_PAGES_KEY: updatedBook.numberOfPages,
           
            IS_AVAILABLE_KEY: updatedBook.isAvailable
        }
        
        if updatedBook.borrower:
            updatedData[BORROWER_KEY] = DBRef(collection= "books", id = updatedBook.borrower)
        else:
            updatedData[BORROWER_KEY] = None
        
        self.db.books.update_one({
            "_id": updatedBook.id
        },
        {"$set": updatedData})
        

    def removeAttributeForBooks(self, isbn, attribute):
         self.db.books.update_one({
            ISBN_KEY: isbn
        },
        
        {"$unset": {
            attribute: ""
        }})
         
    def findBorrowerForBook(self, book):
        books = self.searchBookBy(book.id, None, None, None, None)
        foundBook = books[0]
        #TODO find borrower
        
         
    def searchBookBy(self, id, title, authors, numberOfPages ,isbn):
        filter = {}
        if id:
            filter["_id"] = id
            
        if title:
            filter[BOOK_TITLE_KEY] == title
        
        if authors:
            filter[AUTHORS_KEY] = authors
            
        if numberOfPages:
            filter[NUMBER_OF_PAGES_KEY] = numberOfPages
        
        if isbn:
            filter[ISBN_KEY] = isbn
            
        cursor = self.db.books.find(filter)
        result = []
        for data in cursor:
            borrower = data[BORROWER_KEY]
            borrowerId = None
            if borrower:
                borrowerId = borrower.id
            book = Book(data["_id"],data[BOOK_TITLE_KEY],data[AUTHORS_KEY], 
                        data[ISBN_KEY], data[NUMBER_OF_PAGES_KEY], borrowerId,data[IS_AVAILABLE_KEY] )
            result.append(book)
        
        return result     
        
    def sortBy():
        pass
        
    
def main():
    # dbCommunicator = DbCommunicator()
    # dbCommunicator.createLibraryDatabase()
    library = Library()
    autobio = Book(None, "My Autobiography", ["Travis Zheng"], "1223", 100,None, True)
    # library.addBook(autobio)
    
    travisBorrower = Borrower(None, "Travis Zheng", "travis544", "62635325")
    #library.addBorrower(travisBorrower)
    
    library.checkOutBook(travisBorrower, autobio)
    
    library.findBorrowerForBook(autobio)
    
if __name__ == "__main__":
    main()