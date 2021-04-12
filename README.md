# Convert head position and eye gaze roi on 3D

2021년타사업체의 얼굴 인식 알고리즘의성능을 검증하기 위해,
기존 개발했던 얼굴 인식의 GT데이터와 녹화된 영상으로 관계를 검토 하려한다.
(대외비 관련된 내용은 언급하지 않으려함)

 1. 기존 개발 얼굴인식 GT의 Head position, rotation의 차량,카메라,디스플레이 좌표계 변환 및 검증
 2. 기존 개발 얼굴인식 GT의 Eye gaze를 이용해, Head와 Eye의 최종 vector를 도출
 3. 기존 개발 얼굴인식 GT의 gaze를 이용해, 차량 좌표계상의 3차원 공간들과의 통과 유무 검토(ROI 매칭)
   (앞유리, 사이드 미러, 룸미러, 계기판 등등)
 4. 타사업체의 얼굴 인식 알고리즘의 결과와 기존 개발 얼굴인식의 차이점 검토
 5. 타사업체의 최종 gaze vector를 도출 
 6. ROI 매칭 검토후, accuracy 계산

<img  src = "./desc/coordinate.png"  width="800px" > 

# Gaze ROI 성능 검증 작업 예상일정
기존 제품 차량좌표계, 디스플레이 좌표계, 카메라 좌표계의 차이 파악 및 변환식 검토(~1 weeks)
타사 제품 카메라 좌표계 파악 및 차이점 분석/Eyeclosure 정의 및 iris관련 변환 파악(~1 weeks)
변환 코드 구현 (~1 weeks)
기존 제품 GT데이터를 이용한 Gaze 검증(~1.5 weeks)
기존 제품 GT데이터를 이용한 ROI 검증(~0.5 weeks)
타사 제품 데이터를 이용한 Gaze검증(~1 weeks)
Validataion (~1 weeks)

# 참고문헌
and so on