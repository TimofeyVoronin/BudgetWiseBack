import io
import os
import json
import requests

class ChequeInfo:
    __goodIMGExtension = ("bmp", "gif", "jpeg", "png", "tiff", "pdf")
    __token = os.getenv("TOKEN")       # ваш токен
    __websiteAPI = os.getenv("API")    # URL API proverkacheka

    __columnsName = ("name", "productType", "quantity", "price", "sum")
    __dictProducts = {
        "items": [],
        "data": ""
    }

    def setQRImageFromBytes(self, file_bytes: bytes, filename: str):
        """
        Принимает содержимое файла в виде bytes и его оригинальное имя.
        Отсылает запрос в proverkacheka без сохранения на диск.
        """
        # проверяем расширение
        if not any(filename.lower().endswith(ext) for ext in self.__goodIMGExtension):
            raise NameError(f"Wrong file type, can be only: {', '.join(self.__goodIMGExtension)}")

        files = {
            # requests понимает tuple (filename, fileobj)
            "qrfile": (filename, io.BytesIO(file_bytes))
        }
        data = {"token": self.__token}

        r = requests.post(url=self.__websiteAPI, data=data, files=files)
        resp = r.json()

        if resp.get("code") != 1:
            # сохраняем ошибочный ответ для отладки
            with open("data_failed.json", "w") as outf:
                json.dump(resp, outf, ensure_ascii=False, indent=2)
            raise NameError(f"Error cheque read, error code: {resp.get('code')}")

        # чистим предыдущие результаты
        self.__dictProducts = {"items": [], "data": ""}

        # теперь парсим элементы
        items = resp["data"]["json"]["items"]
        for it in items:
            name = it.get("name", "")
            qty = it.get("quantity", 0)
            price = it.get("price", 0)
            sum_ = qty * price
            self.__dictProducts["items"].append({
                "name": name,
                "productType": "None",
                "quantity": qty,
                "price": price,
                "sum": sum_
            })

        # парсим дату
        self.__dictProducts["data"] = resp["data"]["json"]["dateTime"]

    def getDistProducts(self):
        return self.__dictProducts
