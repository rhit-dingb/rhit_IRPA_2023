
import pandas as pd

class ExcelProcessor():

    def processExcel(self, path, topicToParse):
        data = dict()
        xl = pd.ExcelFile(path)
        enrollmentSubColumns = pd.MultiIndex.from_product([['Full-Time','Part-time'], ["Men", "Woman"]])
        for name in xl.sheet_names: 
            df = xl.parse(name)
          
            topic_key_words = [x.lower() for x in name.split(" ")]
            subName = df.columns[0]
            for topic in topicToParse:
                if topic in topic_key_words:
                    df = df.set_index(subName)
                    index = df.index
                    df_data = df.values
            
                    if("enrollment" in topic_key_words and ("graduate" in topic_key_words or "undergraduate" in topic_key_words) ):
                        # convert to multi index dataframe for full-time and gender
                       
                        df = pd.DataFrame(df_data, columns=enrollmentSubColumns, index = index)
                        df = self.df_to_nested_dict(df)
                    else:
                        df = df.to_dict(orient='index')
                    self.addNewDataInExistingJSON(subName, data, topic, df)
        
        return data



    def addNewDataInExistingJSON(self,subName, data, key, newData):
        if key in data:
            data = data[key] 
        else: 
            data[key] = dict()
            data = data[key]

        if subName.lower() == "unnamed: 0" or subName.lower() == "column1":
            for key in newData:
                #print(key)
                data[key] = newData[key]
        else:
            data[subName] = newData

    #helper to convert enrollment data to json format, represented by python dictionary.
    def df_to_nested_dict(self, df: pd.DataFrame) -> dict:
        d = df.to_dict(orient='index')
        return {k: self.nest(v) for k, v in d.items()}

    def nest(self, dataInDictionaryFormat):
        result = {}
        for key, value in dataInDictionaryFormat.items():
            target = result
            for k in key[:-1]:# traverse all keys but the last
                # will return the reference to the dictionary we passed in as value for k. 
                target = target.setdefault(k, {})
                
            #put in final key in along with the value
            target[key[-1]] = value
            
        return result    