# entities type 

`DATE` # 날짜(아직은 올해 내에서) 오늘을 offset 0으로 두고 특정 날짜를 파악한다. (요일 파악도 추가?)

`LOCATION` # 위치 <이건 어느 정도로 세분화해야할지 고민 좀..>

`TIME` # 24시간 내의 시간을 시/분 오전/오후 등으로 파악

`INGREDIENT` # 요리 재료 (대체 재료? 어울리는 재료 파악 시..?)

`FOOD` # 요리 (이거 어떻게 파악할지 고민..)

`COOKINFO` # 요리 관련 정보? (요리법, 난이도, 양 등 TIP?)

`INGINFO` # 영양성분, 칼로리, 대체재 등의 정보

`FOODINFO` # 완성된 요리 정보?


# Intent 

`greeting` # 인사 (`user name` )

`botself` # 자기소개 / 서비스 안내

`getWeather` # 날씨 알려주는 함수 (`DATE`, `LOCATION` )

`getIngInfo` # 재료 관련 문의 (`INGREDIENT`, `INGINFO` )

`recommandRecipe` # 레시피 추천 () 몇 가지의 프롬프트로 맞춤 추천


