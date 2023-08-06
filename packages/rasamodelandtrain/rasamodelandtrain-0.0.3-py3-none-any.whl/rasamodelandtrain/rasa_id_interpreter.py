#from rasa.nlu.model import Interpreter #Comented by Pravin K on 26-APR-21  [to avoide rasa installation issue] 
import json
import glob
import os
import loggerutility as logger

class Rasa_id_interpreter:
    
    # def __init__(self):
    #     logger.log("init Rasa_id_interpreter ","0")

    @staticmethod
    def get_model_path(enterprise):
        logger.log(f"In get_model_path.[{enterprise}]pwd= {os.getcwd()}","0")
        list_of_files = glob.glob('proteus_services/resources/clients/'+enterprise+'/models/models/*.tar.gz') #Locate latest model file
        latest_file = max(list_of_files, key=os.path.getctime)
        rasa_model_path = latest_file+"/nlu"
        return rasa_model_path

    @staticmethod
    def rasa_output(self,text,attr_count,enterprise):
        logger.log(f"In rasa_output text:{text}","0")
        from rasa.nlu.model import Interpreter  #Added by Pravin K on 26-APR-21 [to avoide rasa installation issue]
        res=[]
        rasa_model_path = self.get_model_path(enterprise)
        interpreter = Interpreter.load(rasa_model_path)
        for t in range(len(text)):
            result = interpreter.parse(text[t])
            entities = result['entities']
            entity_dict = {}
            for j in range(attr_count):
                attr_name = 'attr' + str(j + 1)
                for i in range(len(entities)):
                    if entities[i]['entity'] == attr_name and entities[i]['extractor'] == 'DIETClassifier' and \
                            entities[i]['confidence_entity'] >= 0.90:
                        entity_dict[attr_name] = entities[i]['value']
            res.append(entity_dict)
        return res

    @staticmethod
    def extract_entities(self,products,attr_count,enterprise):
        logger.log(f"In extract_entities[{products}]attr_count[{attr_count}],enterprise[{enterprise}]","0")
        result = []
        entities_extracted = self.rasa_output(self,products,attr_count,enterprise)
        for i in range(len(entities_extracted)):
            attr_list = []
            for j in range(attr_count):
                attr_key = 'attr' + str(j+1)
                attr_list.append(entities_extracted[i].get(attr_key,0))
            text=''
            result_dict={}
            for k in range(len(attr_list)):
                if attr_list[k]!=0:
                    key='attr'+ str(k+1)
                    result_dict[key] = attr_list[k]
            result_dict['descr'] = products[i]
            result_dict['id'] = i+1
            result.append(result_dict)
        return result

    # extract_entities( ["Augmentin 375mg Intravenous"],attr_count=3)