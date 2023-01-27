

from gensim import corpora
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string
from gensim.utils import simple_preprocess
from UnasweredQuestionDBConnector import UnansweredQuestionDbConnector


class Corpus:
    def __init__(self, dataSourceConnector : UnansweredQuestionDbConnector, dictionaryPath):
        self.documents = [
            "He is currently 21 years old, and lives in California",
            "Travis is currently working on a senior project with his teammates, Yiqi, Bowen and Justin",
            "Human machine interface for lab abc computer applications",
            "A survey of user opinion of computer system response time",
            "The EPS user interface management system",
            "System and human system engineering testing of EPS",
            "Relation of user perceived response time to error measurement",
            "The generation of random binary unordered trees",
            "The intersection graph of paths in trees",
            "Graph minors IV Widths of trees and well quasi ordering",
            "Graph minors A survey",
            "A bee is a pollinating animal",
"A bird is a pollinating animal",
"An electrical conductor is a vehicle for the flow of electricity",
"An example of a change in the Earth is an ocean becoming a wooded area",
"An example of a chemical change is acid breaking down substances",
"An example of a fossil is a footprint in a rock",
"An example of a fossil is a paw print in rock",
"An example of a fossil is the bones of an extinct animal",
"An example of a mixture is clay mixed together",
"An example of a reproductive behavior is salmon returning to their birthplace to lay their eggs",
"An example of a seasonal change is an animal growing thick fur for keeping warm in the winter",
"An example of a seasonal change is plants becoming dormant in the winter",
"An example of a seasonal change is plants dying in the winter",
"An example of an adaptation is camel humps",
"An example of an inherited behavior is a bird building a nest",
"An example of an instinct is the kangaroo 's ability to crawl into its mother 's pouch to drink milk",
"An example of an instinctive behavior is a baby bird pecking at its shell to hatch",
"An example of avoiding waste is using a material more than once",
"An example of avoiding waste is using an object more than once",
"An example of camouflage is an organism looking like leaves",
"An example of camouflage is when an organism looks like its environment",
"An example of camouflage is when something changes color in order to have the same color as its environment",
"An example of camouflage is when something has the same color as its environment",
"An example of camouflage is when something is the same color as its environment",
"An example of collecting data is measuring",
"An example of combining two substances is pouring one substance into the other substance",
"An example of conservation is avoiding waste",
"An example of conservation is not using fossil fuel",
"An example of creating an alternative fuel is turning plant material into fuel",
"An example of evaporation is a body of water drying up by absorbing heat energy",
"An example of hibernation is a frog burying itself in mud",
"An example of hitting something is dropping an object onto that something",
"An example of hunting is an otter cracking open clams with a rock",
"An example of migration is birds flying south in the winter",
"An example of moisture is water vapor in the atmosphere",
"An example of navigation is directing a boat",
"An example of playing a musical instrument is hitting the keys of a piano",
"An example of playing a musical instrument is strumming a guitar string",
"An example of protecting the environment is creating protected areas",
"An example of protecting the environment is reducing the amount of pollutants",
"An example of protecting the environment is reducing the amount of waste",
"An example of recycling is using an object to make a new object",
"An example of replacing a natural resource is planting new trees where a forest once stood",
"An example of reproduction is laying eggs",
"An example of seed dispersal is animals eating seeds",
"An example of seed dispersal is is an animal gathering seeds",
"An example of stormy weather is rain",
"An example of using tools is a chimpanzee digging for insects with a stick",
"An example of weathering is when a plant root grows into a crack in rock",
"An insect is a pollinating animal",
"August is during the winter in the southern hemisphere",
"DNA is a vehicle for passing inherited characteristics from parent to offspring",
"December is during the summer in the southern hemisphere",
"December is during the winter in the northern hemisphere",
"Earth 's magnetic patterns are used for finding locations by animals that migrate",
"Earth 's surface is made of rock",
"Earth 's tilt on its axis causes seasons to occur",
"Earth is made of rock",
"Earth is the planet that is third closest to the Sun",
"Earth orbiting the Sun causes seasons to change",
"Galileo Galilei made improvements to the telescope to make better observations of celestial bodies",
"In the cellular respiration process carbon dioxide is a waste product",
"In the food chain process a green plant has the role of producer",
"In the food chain process an animal has the role of consumer which eats other animals for food",
"In the food chain process an animal has the role of consumer which eats producers for food",
"In the food chain process bacteria have the role of decomposer",
"In the food chain process fungi have the role of decomposer",
"In the food chain process some types of plankton have the role of producer",
"In the photosynthesis process carbon dioxide has the role of raw material",
"In the photosynthesis process oxygen has the role of waste product",
"In the respiration process carbon dioxide is a waste product",
"In the tree reproduction process a squirrel has the role of seed disperser",
"January is during the winter in the northern hemisphere",
"June is during the summer in the northern hemisphere",
"June is during the winter in the southern hemisphere",
"Louis Pasteur invented pasteurization",
"Matter in the gas phase has variable shape",
"Matter in the gas phase has variable volume",
"Matter in the liquid phase has definite volume",
"Matter in the liquid phase has variable shape",
"Matter in the solid phase has definite shape",
"Pluto is the planet that is ninth closest to the Sun",
"Vitamin D heals bones",
"a Punnett square is used to identify the percent chance of a trait being passed down from a parent to its offspring",
"a Rotation of the Earth on Earth 's axis takes 1 day",
"a Rotation of the Earth on itself takes one day",
"a balance is used for measuring mass of an object",
"a balance is used for measuring weight of a substance",
"a balloon contains gas",
"a barometer is used to measure air pressure",
"a bat births live young",
"a battery converts chemical energy into electrical energy",
"a battery is a source of electrical energy",
"a beach ball contains gas",
"a beak is used for catching prey by some birds",
"a berry contains seeds",
"a bicycle contains screws",
"a bird is warm-blooded",
"a body of water is a source of water",
"a bubble contains gas",
"a cactus stem is used for storing water",
"a cactus stores water",
"a camera is used for recording images",
"a candle is a source of light when it is burned",
"a canyon forming occurs over a period of millions of years",
"a canyon is made of rocks",
"a car engine is a source of heat",
"a car engine usually converts gasoline into motion and heat through combustion",
"a carbonated beverage contains dissolved carbon dioxide",
"a cavern is formed by carbonic acid in groundwater seeping through rock and dissolving limestone",
"a chipmunk eats acorns",
"a chloroplast contains chlorophyll",
"a closed circuit has continuous path",
"a community is made of many types of organisms in an area",
"a compass 's needle lines up with Earth 's magnetic poles",
"a compass is a kind of tool for determining direction by pointing north",
"a compass is used to navigate oceans",
"a compass is used to navigate seas",
"a complete electrical circuit is a source of electrical energy",
"a complete revolution of the Earth around the sun takes one Earth year",
"a complete revolution of the Earth around the sun takes one solar year",
"a computer controls a robot",
"a consumer can not produce its own food",
"a cycle happens repeatedly",
"a cycle occurs repeatedly",
"a decrease in visibility while driving can cause people to crash their car",
"a deer lives in a forest",
"a dense forest environment is often dark in color",
"a desert environment contains very little food",
"a desert environment has low rainfall",
"a desert environment is dry",
"a desert environment is low in availability of water",
"a desert environment is usually hot in temperature",
"a desert environment usually has a lot of sunlight",
"a different moon phase occurs once per week",
"a disperser disperses",
"a doorbell converts electrical energy into sound",
"a female insect lays eggs during the adult stage of an insect 's life cycle",
"a fish lives in water",
"a flashlight converts chemical energy into light energy",
"a flashlight emits light",
"a flashlight requires a source of electricity to produce light",
"a flower 's purpose is to produce seeds",
"a flower is a source of nectar",
"a flower produces pollen and seeds",
"a force acting on an object in the opposite direction that the object is moving can cause that object 's speed to decrease in a forward motion",
"a force continually acting on an object in the same direction that the object is moving can cause that object 's speed to increase in a forward motion",
"a forest environment is often green in color",
"a forest environment receives more rainfall than a desert",
"a frog eats insects",
"a glacier causes mechanical weathering",
"a glacier is made of ice",
"a glacier moves slowly",
"a graduated cylinder is a kind of instrument for measuring volume of liquids or objects",
"a graduated cylinder is used to measure volume of an object",
"a grassland environment receives more rainfall than a desert",
"a greenhouse is used to protect plants by keeping them warm",
"a greenhouse is used to protect plants from the cold",


        ]
        # processedDoc = self.preprocessDocuments(self.documents)
        # self.dictionary = corpora.Dictionary(processedDoc)
        # self.dataSourceConnector = dataSourceConnector
        # self.dictionaryPath = dictionaryPath

    def constructDictionary(self):
       self.dictionary = corpora.Dictionary(doc for doc in self)


    # MAYBE MAKE AN DB CALL HERE
    def __len__(self):
        return len(self.documents)

    def preprocessDoc(self,doc): 
        # processDocument = remove_stopwords(doc)
        processDocument = doc
       
        # processDocument = preprocess_string(processDocument)
        processDocument = simple_preprocess(processDocument)
        
        return processDocument

    def preprocessDocuments(self,documents):
        processedDocuments = []
        for doc in documents:
            processDoc = self.preprocessDoc(doc)
            processedDocuments.append(processDoc)
        # print(processedDocuments)
        return processedDocuments   


    def addDocuments(self,documents):
        preprocessedDocuments = self.preprocessDocuments(documents)
        # Add document to database---currently add to list, but probably will replace this with call to database.
        self.documents = self.documents + documents
        self.updateDictionary(preprocessedDocuments)

    # #Probably replace this with database call.
    def getDocumentByIndex(self, doc_position):
        return self.documents[doc_position]

    def retrieveDocumentFromDataSource(self):
        # Probably replace this with a database call.
        for doc in self.documents:
            yield doc

        

    def updateDictionary(self,documents):
        self.dictionary.add_documents(documents)

    
    def loadDictionary(self,path):
        self.dictionary = corpora.Dictionary.load(path)

    def saveDictionary(self, path):
        self.dictionary.save(path)
    
    def __iter__(self):
        for doc in self.retrieveDocumentFromDataSource():
            # yield self.convertDocToBow(doc)
            preprocessDoc = self.preprocessDoc(doc)
            yield preprocessDoc

    def convertDocToBow(self,doc):
        return self.dictionary.doc2bow(doc)