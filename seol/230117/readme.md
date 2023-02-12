## 설종명 부사장 태조엔지니어링

기존의 단면검토프로그램을 Excel에서 인풋 및 아웃풋하도록 수정
openpyxl 이용.

branch : seolxlwings
* 이 브랜치에서는 xlwings를 이용해서 input파일(Calc_As_input_xlwings.xlsx)에서 입력을 한 후 그 파일에 케이스별로 out을 하도록 수정함. 230212

* 입력형식은 재료(fck,fy), 계수(pic,pis), 단면/하중/사용철근경우 세그룹으로 구성.

* 여러개의 데이터를 입력할 수 있도록 했으며, 검토케이스 이름을 시트명으로 해서 아웃풋이 만들어짐.

