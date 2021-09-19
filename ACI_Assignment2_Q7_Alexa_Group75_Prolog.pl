/*ACI Assignment 2 - Q7 - Alexa
Alexa Dataset
Group number - 75

Members name:
Nareshkumar P (2020fc04122@wilp.bits-pilani.ac.in)
Kommajyosula VNS Kanth (2020FC04120@wilp.bits-pilani.ac.in)
T Navya Madhavi (2020FC04007@wilp.bits-pilani.ac.in)
Avi Krishna Srivatsava (2020FC04492@wilp.bits-pilani.ac.in)
Dola Tejesh (2020FC04459@wilp.bits-pilani.ac.in)*/

/*Defing Rating*/
rating(1).
rating(2).
rating(3).
rating(4).
rating(5).

/*Define Variation*/
variation(CharcoalFabric).
variation(WalnutFinish).
variation(HeatherGrayFabric).
variation(SandstoneFabric).
variation(OakFinish).
variation(Black).
variation(White).
variation(BlackSpot).
variation(WhiteSpot).
variation(BlackShow).
variation(WhiteShow).
variation(BlackPlus).
variation(WhitePlus).
variation(Configuration:FireTVStick).
variation(BlackDot).
variation(WhiteDot).

/*Define Date*/
date(january).
date(february).
date(march).
date(april).
date(may).
date(june).
date(july).
date(august).
date(september).
date(october).
date(november).
date(december).

/*Define Feedback*/
feedback(1).
feedback(0).

/*Implement Decession Tree Rule flow 

|--- If Rating <= 2 and Date in (january,february,march,april,may,june,july,august,september,october,november,december) and Variation in (CharcoalFabric,WalnutFinish,HeatherGrayFabric,SandstoneFabric,OakFinish,Black,White,BlackSpot,WhiteSpot,BlackShow,WhiteShow,BlackPlus,WhitePlus,Configuration:FireTVStick,BlackDot,WhiteDot)
|   |--- Feedback: 0
|--- If Rating >  2 and Date in (january,february,march,april,may,june,july,august,september,october,november,december) and Variation in (CharcoalFabric,WalnutFinish,HeatherGrayFabric,SandstoneFabric,OakFinish,Black,White,BlackSpot,WhiteSpot,BlackShow,WhiteShow,BlackPlus,WhitePlus,Configuration:FireTVStick,BlackDot,WhiteDot)
|   |--- Feedback: 1 

*/



 
/* -Derived Rules

If Rating =1 and Date in (list_of_months) and Variation in (list_of_variations) then Feedback=0 (Negative Feedback)
If Rating =2 and Date in (list_of_months) and Variation in (list_of_variations) then Feedback=0 (Negative Feedback)
If Rating =3 and Date in (list_of_months) and Variation in (list_of_variations) then Feedback=1 (Positive Feedback)
If Rating =4 and Date in (list_of_months) and Variation in (list_of_variations) then Feedback=1 (Positive Feedback)
If Rating =5 and Date in (list_of_months) and Variation in (list_of_variations) then Feedback=1 (Positive Feedback)

*/

/*is_feedback_positive(X,Y,Z) :- rating(X) = rating(3), date(Z) = date(september), variation(Y) = variation(BlackSpot).*/

/*Prolog Rules code 
X -> Rating
Y -> Variation
Z -> Month as Date*/
is_feedback_positive(X,Y,Z) :- rating(X) = rating(3), member(Z,[january,february,march,april,may,june,july,august,september,october,november,december]), member(Y,[CharcoalFabric,WalnutFinish,HeatherGrayFabric,SandstoneFabric,OakFinish,Black,White,BlackSpot,WhiteSpot,BlackShow,WhiteShow,BlackPlus,WhitePlus,Configuration:FireTVStick,BlackDot,WhiteDot]).
is_feedback_positive(X,Y,Z) :- rating(X) = rating(4), member(Z,[january,february,march,april,may,june,july,august,september,october,november,december]), member(Y,[CharcoalFabric,WalnutFinish,HeatherGrayFabric,SandstoneFabric,OakFinish,Black,White,BlackSpot,WhiteSpot,BlackShow,WhiteShow,BlackPlus,WhitePlus,Configuration:FireTVStick,BlackDot,WhiteDot]).
is_feedback_positive(X,Y,Z) :- rating(X) = rating(5), member(Z,[january,february,march,april,may,june,july,august,september,october,november,december]), member(Y,[CharcoalFabric,WalnutFinish,HeatherGrayFabric,SandstoneFabric,OakFinish,Black,White,BlackSpot,WhiteSpot,BlackShow,WhiteShow,BlackPlus,WhitePlus,Configuration:FireTVStick,BlackDot,WhiteDot]). 


/*Input Test*/
myinput :- 
write('Enter Details'),
write('Enter Rating: <1/2/3/4/5>?'), read(X),
write('Enter Month: <january/februaury/march/.../december>?'), read(Y),
write('Enter variation: <CharcoalFabric/WalnutFinish/HeatherGrayFabric/SandstoneFabric/OakFinish/Black/White/BlackSpot/WhiteSpot/BlackShow/WhiteShow/BlackPlus/WhitePlus/Configuration:FireTVStick/BlackDot/WhiteDot>?'), read(X),
is_feedback_positive(X,Y,Z).

