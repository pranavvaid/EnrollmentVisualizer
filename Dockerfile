FROM python:3
ADD collectcourses.py /
ADD stanfordclasses.py /
#ADD cardinaldirection.py /
#ADD stanfordclasslist.pkl /
#ADD departmentstograph.txt /
#ADD coursemap.py /
ADD processClassEnrollments.py /
ADD stanfordclasslistBEFOREANNOUNCEMENTv2.pkl /
ADD stanfordclasslistAFTERANNOUNCEMENT3-28.pkl /
ADD stanfordclasslistAFTERANNOUNCEMENT3-30.pkl /
ADD stanfordclasslistAFTERANNOUNCEMENT3-31.pkl /
ADD stanfordclasslistAFTERANNOUNCEMENT04_02_01_12_25.pkl / 
ADD stanfordclasslistAFTERANNOUNCEMENT04_02_21_38_36.pkl /
RUN mkdir /pickles
#RUN pip install requests
#RUN pip install xmltodict
#RUN pip install networkx
#RUN pip install beautifulsoup4
#RUN pip install --upgrade 'algoliasearch>=2.0,<3.0'
RUN pip install pandas
RUN pip install plotly
#CMD [ "python", "./cardinaldirection.py"]
#CMD [ "python", "./collectcourses.py"]
#CMD [ "python", "./coursemap.py"]
CMD ["python", "./processClassEnrollments.py"]