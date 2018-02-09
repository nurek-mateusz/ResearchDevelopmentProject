# A simple guide to fill Elasticsearch with data from Jira

## Files needed to proceed further
### 1. Elasticsearch
* **download** from [**this link**](https://www.elastic.co/downloads/elasticsearch)
* **unzip** files

### 2. Logstash
* **download** from [**this link**](https://www.elastic.co/downloads/logstash)
* **unzip** files
* copy **jira-pipeline.conf** to **Logstash/bin** directory
* copy **rest_client.py** **Logstash/bin** directory
	
### 3. Python interpreter (3.\*.\*)
* **download** from [**this link**](https://www.python.org/downloads/release/python-363/)
* **execute** or **unzip** files
*	**download REQUEST LIBRARY**
	* Run **python -m pip install requests** 
### 4. Postman App, cURL or another rest client
	
## Steps to fill Elasticsearch
	
1. Go to **Elasticsearch/bin** directory

2. Run **elasticsearch** or **elasticsearch.bat** (on Windows)

3. To check if everything is working -> [**click this**](http://localhost:9200/)

4. If web browser **presents** data about Elasticsearch, we can proceed to next step  
	if not, check first section about needed files and repeat 1-3 steps from second section
5. Go to **Logstash/bin** directory

6. Run python script, e.g **python rest_client.py**, this should generate new file **jira.xml**

7. Open **jira-pipeline.conf** file via text editor, find line 7 _path =>..._, replace **[PATH_TO_A_DIRECTORY]** with a **path to Logstash/bin** 

8. Run Logstash **config** file 
	1. **logstash -f jira-pipeline.conf --config.test_and_exit** -> to verify configuration file
	
	2. **logstash -f jira-pipeline.conf --config.reload.automatic** -> to automatic config reloading
		* (**IF NEEDED**) If 8 step went wrong, to repeat -> delete Logstash\data\plugins\inputs\file\\*
9. Executed 8.2 command from the last step should populate Elasticsearch and stop at the last entry (issue),  
	it is waiting for the next file/data. We dont have more files so we need to exit Logstash -> **Ctrl+C**

10. Based on which rest client we chose, now we are going to get some data from Elasticsearch
	
	1. Send **POST http://localhost:9200/_search** request
		* (**IMPORTANT**) **Set** content-type -> application/json
		
		* This should get all data that we transfered to Elasticsearch
		* (**IF NEEDED**) **DELETE http://localhost:9200/_all** request to delete all data in Elasticsearch
			