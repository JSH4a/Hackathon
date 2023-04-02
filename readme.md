DB Interactions Schema:

(Note: must instantiate as class, then call db.close once done to save 
changes.)

addProduct(String productName, Float Emissions, String tags)
//adds a product to the database

addCompany(String productName, Float Emissions, String tags)
//adds a company to the database

getProductsWithRange(int range)
//gets products as close in emissions as the range i.e. smaller range = 
more difficult, greater = less
returns a tuple in the form  ((product1 id, product1 name, product1 
emissions), (product2 id, product2 name, product2 emissions)) in 
randomised order


updateTimesSeen(int id, int correctGuesses, int totalGuesses)
//updates the number of times seen for a given product with correct 
guesses and total guesses

getPrevResults(int id):
returns a tuple in the form of (int correctGuesses, int TotalGuesses)


