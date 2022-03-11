# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies0103

    def process_item(self, item, spider):
        # print(item['salary'])
        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'] = self.process_salary(item['salary'])
            del item['salary']
        elif spider.name == 'superjob':
            item['min'], item['max'], item['cur'] = self.process_salary_sj(item['salary'])
            del item['salary']

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):

        salary_data_cleared = [elem.replace("\xa0", '') for elem in salary]
        salary_data_cleared = [elem.replace(" до ", 'до ') for elem in salary_data_cleared]

        try:
            upto_index = salary_data_cleared.index('до ')
        except ValueError:
            upto_index = None

        try:
            from_index = salary_data_cleared.index('от ')
        except ValueError:
            from_index = None

        if upto_index is not None:
            max_salary = int(salary_data_cleared[upto_index + 1])
        else:
            max_salary = None

        if from_index is not None:
            min_salary = int(salary_data_cleared[from_index + 1])
        else:
            min_salary = None

        currency = salary_data_cleared[-2]

        return min_salary, max_salary, currency

    def process_salary_sj(self, salary):

        # salary_data_cleared = [elem.replace("\xa0", '') for elem in salary]

        if "от" in salary:

            salary_data_prepared = salary[2].replace("\xa0", '', 1)
            salary_data_split = salary_data_prepared.split("\xa0")
            min_salary = int(salary_data_split[0])
            max_salary = None
            currency = salary_data_split[1]

        elif "—" in salary:
            min_salary = int(salary[0].replace("\xa0", ''))
            max_salary = int(salary[4].replace("\xa0", ''))
            currency = salary[-1]

        else:
            min_salary = None
            max_salary = None
            currency = None

        return min_salary, max_salary, currency
