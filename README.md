### 수정 된 것

____

**[1] TmpPicture => 로그인 안하고 딥러닝 돌렸을 때 사용되는 Model**

`TmpPictureList(APIView)` 에서 POST 함수를 이용하여 클라이언트와 통신

**간단 요약**

1. 클라이언트 requset(POST)
2. request 데이터 검증  
3. 검증 완료시 이미지 데이터를 일단 저장
4. 저장된 이미지를 이용하여 Style Transfer 
5. 결과 이미지 저장 
6.  결과 이미지를 불러와서 base64 인코딩
7. 그 데이터를 포함하여 클라이언트에게 response



**[2] uploads, results 폴더**

업로드 된 이미지와 style-transfer 된 이미지가 결과로 저장



**[3] 딥러닝 관련 파일들**

1. 파이썬 파일

   `transfer.py`, `transfer_net.py`, `util.py`

2. 관련 폴더

   ` parameter`  



## 실행

1. pip3 install -r requirements.txt
2. python3 manage.py makemigrations
3. python3 manage.py migrate —run-syncdb
4. python3 manage.py createsuperuser
5. python3 manage.py runserver