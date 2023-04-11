from typing import Any, Dict, List
from haystack import Label, Document
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel
from haystack.nodes import  EmbeddingRetriever, BM25Retriever, BaseRetriever
from haystack.nodes.question_generator import QuestionGenerator
from Knowledgebase.DataModels.FeedbackLabel import FeedbackType
from haystack.nodes.label_generator import PseudoLabelGenerator

class Trainer:
    def __init__(self):
        self.trainingDataCreator = TrainingDataCreator()
        # Download the model 
        questionAnswerPair = [{"question":"What is my name", "document": "Travis Zheng"}]
        self.questions_producer = QuestionGenerator(model_name_or_path="doc2query/msmarco-t5-base-v1", 
                                         max_length=64, 
                                         split_length=128, 
                                         batch_size=32,
                                         num_queries_per_doc=3)
        labelGenerator = PseudoLabelGenerator(question_producer=self.questions_producer, retriever=BM25Retriever())
    

    
    def trainDataForEmbeddingRetriever(self,  trainingLabels : List[MultiFeedbackLabel], retriever : EmbeddingRetriever, saveDirectory : str ,documentStore, source : str = None):
        filteredTrainingData = []
        if not source == None: 
            for container in trainingLabels:
                fitleredFeedbackLabels = []
                for singleFeedbackLabel in container.feedbackLabels:
                    if singleFeedbackLabel.source == source:
                        fitleredFeedbackLabels.append(singleFeedbackLabel)

                newMultiFeedbackLabel = MultiFeedbackLabel(container.query, fitleredFeedbackLabels)
                filteredTrainingData.append(newMultiFeedbackLabel)

        trainingData = self.trainingDataCreator.createTrainingDataForEmbeddingRetriever(filteredTrainingData, retriever, documentStore)
        print("USE THIS AS TRAINING DATA", trainingData)
        retriever.train(training_data=trainingData, n_epochs = 1, num_workers=2, train_loss="mnrl")
        retriever.save(saveDirectory)
        return True

class TrainingDataCreator:
    def __init__(self):
        self.questions_producer = QuestionGenerator(model_name_or_path="doc2query/msmarco-t5-base-v1", 
                                         max_length=64, 
                                         split_length=128, 
                                         batch_size=32,
                                         num_queries_per_doc=3)



    def createTrainingDataForEmbeddingRetriever(self, trainingLabels : List[MultiFeedbackLabel], retriever : EmbeddingRetriever, documentStore) -> List[Dict[str, Any]]:
        """
        Tutorial to how to train the embedding retriever: https://colab.research.google.com/drive/1Tz9GSzre7JfvXDDKe7sCnO0FMuDViMnN?usp=sharing#scrollTo=ad4b870e
        The training data for embedding retriever looks like:
        Each training data example is a dictionary with the following keys:
        * question: the question string
        * pos_doc: the positive document string
        * neg_doc: the negative document string
        * score: the score margin

        :return: A list of dictionaries, each of which has the following keys:
            - question: The question string
            - pos_doc: Positive document string
            - neg_doc: Negative document string
            - score: The score margin
        """
        embeddingRetrieverTrainingData = []

        questionDocumentPair = []
        questionToPositiveDocument=[]
        for trainingLabel in trainingLabels:
            query = trainingLabel.query
            trainingData = dict()
            trainingData["question"] = query
            pos_docs = []
            neg_docs= []
            for feedbackLabel in trainingLabel.feedbackLabels:
                content = feedbackLabel.metadata["document_content"]
                if feedbackLabel.feedback == FeedbackType.CORRECT:
                    pos_docs.append(content)
                    questionToPositiveDocument.append({"question": feedbackLabel.query, "document":content})
                elif feedbackLabel.feedback == FeedbackType.INCORRECT:
                    neg_docs.append(feedbackLabel.metadata["document_content"])

                questionDocumentPair.append({"question":feedbackLabel.query, "document":feedbackLabel.answerProvided})

                # print("THIS IS THE training data")
                print(feedbackLabel.__dict__)

        # print("THIS IS THE PAIR")
        # print(questionAnswerPair) 
        
       
        # I will use this create score margins rather than auto generate labels.
        labelGenerator = PseudoLabelGenerator(question_producer=self.questions_producer, retriever=retriever)
        # labelGenerator.generate_questions()


        dataToGetScoreMarginFor = []
        # Generate every possible combination of pos_doc and negative_doc:
        for trainingLabel in trainingLabels:
            for pos_doc in pos_docs:
                for neg_doc in neg_docs:
                    data = {"question": trainingLabel.query, "pos_doc":pos_doc, "neg_doc": neg_doc}
                    dataToGetScoreMarginFor.append(data)

        # dataMined= labelGenerator.mine_negatives(questionToPositiveDocument)
        # dataMined, pipe_id  = labelGenerator.run([Document(content=trainingLabel.query) for trainingLabel in trainingLabels])
        dataMined, pipe_id = labelGenerator.run(documentStore.get_all_documents(filters={"startYear":"2020", "endYear":"2021"}))
        # print("DATA MINED")
        # print(dataMined)
        dataToGetScoreMarginFor = dataToGetScoreMarginFor
        embeddingRetrieverTrainingData = labelGenerator.generate_margin_scores(dataToGetScoreMarginFor)

        embeddingRetrieverTrainingData = embeddingRetrieverTrainingData+dataMined["gpl_labels"]
        print("EMBEDDING TRAINING DATA")
        print(embeddingRetrieverTrainingData)
        return embeddingRetrieverTrainingData

          
                