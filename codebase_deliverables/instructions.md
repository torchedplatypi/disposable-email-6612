This read me will guide you all of the code created for this project.

Note that many of these commands include writing files, so sudo may be necessary.
# Part 0: Setting up the Environment
This projected is disigned to be run with python3. To set up the environment for the project, you will first need to have python3 and pip3 installed in the VM. The usage of virtualenv is strongly recommended. 
#### Run: 
pip3 install virtualenv
virtualenv disposable_email_env
source disposable_email_env/bin/activate
These steps above will create a new virtualenv named disposable_email_env and will set up the python enviroment accordingly. 
#### Run:
pip install -r requirements
This step installs all the necessary packages and dependencies in the virtual environment
# Part 1: Crawling and Parsing
We created crawlers for both guerrillamail and mailinator. This will walk you through how to handle crawling and parsing for mailinator,
but guerrilla mail is very similar.

After installing all requirements, change your directory to src/crawl_and_parse.

#### Run:
python main_mailinator.py t

The argument t specifies that you do not want html in your data, which is how we went about the project.

This will load emails from this day, and place their data in a csv in a folder under mailinator_data. **(Occasionally this step fails because of bad data loaded into the mailinator API but it almost always runs.)**

If you look in the mailinator_data folder you should see a file with today's date and csv extension that has the data loaded from mailinator. Repeating the above command will add to this csv file (until the date changes and a new csv is made).

To parse this data into a format that we can work with, you can run the following from the src/crawl_and_parse folder.

#### Run:
python email_parser.py mailinator_data

This will create a new folder called training_data/mailinator_data/{today's date} in the current directory that has information about each email split into separate files. We will similar data later to classify with unsupervised machine learning.

If you wish to run the crawler and parser with guerrilla mail you simply have to run the main.py program which will crawl the website and then call email_parser.py with guerrilla_data as the extension (no "t" argument).

# Part 2: Unsupervised Machine Learning

We have provided pre-parsed data that can be used as the input to the unsupervised machine learning algorithm. To run this, change into the src/unsupervised_classifier folder. From there, run the following code.

#### Run:
python unsupervised_classifier.py -d "../../data/training_data/mailinator_data/4-5-2019/" 4

The first argument specifies the path to the data. The second argument specifies the number of clusters you wish to create (the "k" in k-means clustering). Note: 8 is the maximum allowable value for k.

This will script will create k output files that list the features and their scores for each cluster. It will also produce a chart saved in Cluster_DataSet.png which is a plot created with PCA.

# Part 3: Classifying Emails

This section will show you how to take a csv file of emails and determine which our whole classifier believes to be phishing. Previous parts are not required as we have already created the necessary files and stored them in data. Start by changing into the src/suspicious_classifier folder.

#### Run:
python (this will enter you into the python command line)

import SuspiciousClassifier

x = SuspiciousClassifier.SuspiciousClassifier(28, 3)

x.set_filename("../../data/mailinator_data/4-5-2019.csv")

x.set_freq_data("../../data", ["Cluster_0_Features.txt", "Cluster_1_Features.txt", "Cluster_2_Features.txt", "Cluster_3_Features.txt"])

x.read_file()

This will do the following:
1) import the suspicious classifier module
2) create an instance of the suspicious classifier where the max amount of emails to parse is 100 and cluster #2 (Cluster_1_Features.txt) has been determined to be the phishing cluster.
3) set the path to the cluster feature information
4) begin running

Once this has terminated, you can proceed.

#### Run:
exit()

This will return you to the terminal. Here there will be two outputs, a pie chart showing how the emails have been classified, and a file called high_threat_output. which contains the bodies of the emails which are most likely to be phishing.

