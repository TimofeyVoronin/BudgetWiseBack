from llama_cpp import Llama
import json
from app.input_Protect.middleware import MiddleWare


class AutoFillLLM(MiddleWare):
    '''__llm = Llama.from_pretrained(
       	repo_id="bartowski/Ministral-8B-Instruct-2410-GGUF",
	    filename="Ministral-8B-Instruct-2410-Q4_K_S.gguf",
    )'''


    #Take name from all items in cheque
    def __getItems(self,jsonImput):
        productList = []
        for i in range(len(jsonImput.items)):
            productList.append(jsonImput.items[i]["name"])
        return productList

    def getCategory(self,jsonImput,transactionID):
    
        listProducts = self.__getItems(jsonImput)#Get items from chequeInfo

        #Set initional information in LLM for distribution of categories
        '''response = self.__llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": f"Ты помощник учета финансов, твоя задача определить к какому виду расходов относится входящий чек {listProducts}.\
                    На вход поступает массив позиций товаров/услуг в чеке.\
                        У тебя имются следующие виды расходов:\
                            0.<Обязательные расходы> - к ним относится оплата квартиры, коммунальных платежей и т.д.;\
                            1.<Расходы на питание> - оплата продуктов в магазине, на рынке, питание в кафе, ресторанах, столовых и т.д.;\
                            2.<Расходы на хозяйственно бытовые нужды> - ремонт одежды, обуви  т.д., также покупка предметов личной гигиены;\
                            3.<Расхды на предметы личного пользования> - одежда, обувь, постельные принадлежности и т.д.;\
                            4.<Расходы на предметы быта> - мебель, светильники, часы, хрусталь и т.д..;\
                            5.<Прочее> - все что не подходит под остальные категории\
                                В качестве ответа выбери вид расходов и запиши его номер в category json. В случае если не все товары в чеке относится к одной категории,\
                                    то поставь доминирующию категорию расходов которых больше всего"
                    
            },
        
        ],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"categoria":{"type":int}},
                "required": ["categoria"],
            },
        },
        temperature=0.2 #For small random from LLM
        )

        js = json.loads(response["choices"][0]["message"]["content"])
        js["id"]=transactionID
        
        return json.dumps(js)'''
        
        return {"categoria":"Прочее","id":transactionID}#Delete
    
    def getPrositionCategory(self,jsonImput):

        listProducts = self.__getItems(jsonImput)#Get items from chequeInfo

        #Set initional information in LLM for distribution of productType
        '''response = self.__llm.create_chat_completion(
        messages=[
            {

                "role": "user",
                "content": f"Ты помощник учета финансов, твоя задача определить к какому виду товаров/услуг относится каждый элемент входящего чека: {listProducts}.\
                    На вход поступает массив позиций товаров/услуг в чеке.\
                        У тебя имются следующие виды расходов:\
                            0.<Обязательные расходы> - к ним относится оплата квартиры, коммунальных платежей и т.д.;\
                            1.<Расходы на питание> - оплата продуктов в магазине, на рынке, питание в кафе, ресторанах, столовых и т.д.;\
                            2.<Расходы на хозяйственно бытовые нужды> - ремонт одежды, обуви  т.д., также покупка предметов личной гигиены;\
                            3.<Расхды на предметы личного пользования> - одежда, обувь, постельные принадлежности и т.д.;\
                            4.<Расходы на предметы быта> - мебель, светильники, часы, хрусталь и т.д..;\
                            5.<Прочее> - все что не подходит под остальные категории\
                                В качестве ответа напиши массив, который будет содежать цифру категории каждого вида товаров/услуг для каждого элемента чека и запиши это в json."

            },
        ],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"categoryID":[{"type":int}]},
                "required": ["productType"],
            },
        },
        temperature=0.2
        )

        #Sometimes LLM distort the names of listItems, then take only values of keys
        js = list(json.loads(response["choices"][0]["message"]["content"]).values())

        #set productType in jsonImput
        for i in range(len(listProducts)):
            
            jsonImput.items[i]["categoryID"] = js[i]


        return json.dumps(jsonImput)'''
        return {jsonImput}#Delete